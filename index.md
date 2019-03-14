---
layout: home
debug: false
---
<style>.embed-container { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; } .embed-container iframe, .embed-container object, .embed-container embed { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }</style>

{% assign first_post = site.data.posts.first[1] %}
# Posts by ![Profile photo of {{ first_post.author.displayName }}]({{ first_post.author.avatarImageUrl }}) {{ first_post.author.displayName }}
{% assign posts = "" | split:'' %}
{% assign site_posts = site.data.posts %}
{% assign public_posts = site_posts | where_exp: "post", 'post.postAcl.isPublic == true' %}

Found: {{ site_posts | size }} posts of which {{ public_posts | size }} are public. Listing public posts:




{% assign counter = 0 %}
{% for post in public_posts reversed %}
{% assign audiences = "" | split: ',' %}
{% assign circle_types = post.postAcl.visibleToStandardAcl.circles | map: 'type' %}
{% assign circle_display_names = post.postAcl.visibleToStandardAcl.circles | map: 'displayName' %}
{% if circle_types contains 'CIRCLE_TYPE_PUBLIC' %}{% assign audiences = audiences | push: 'Public' %}{% endif %}
{% if circle_types contains 'CIRCLE_TYPE_EXTENDED_CIRCLES' %}{% assign audiences = audiences | push: 'Extended Circles' %}{% endif %}
{% if circle_types contains 'CIRCLE_TYPE_YOUR_CIRCLES' %}{% assign audiences = audiences | push: "{{ first_post.author.displayName }}'s circles" %}{% endif %}
{% if circle_types contains 'CIRCLE_TYPE_USER_CIRCLE' %}{% assign audiences = audiences | concat: circle_display_names %}{% endif %}

{% if post.postAcl.collectionAcl.collection.displayName %}
{% assign audiences = audiences | push: post.postAcl.collectionAcl.collection.displayName %}
{% endif %}

{% if post.postAcl.communityAcl %}
{% if post.postAcl.communityAcl.community.displayName %}
{% assign audiences = audiences | push: post.postAcl.communityAcl.community.displayName %}
{% else %}
{% assign audiences = audiences | push: 'UNTITLED_COLLECTION' %}
{% endif %}
{% endif %}

{% if post.postAcl.eventAcl %}
{% if post.postAcl.eventAcl.event.displayName %}
{% assign audiences = audiences | push: post.postAcl.eventAcl.event.displayName %}
{% else %}
{% assign audiences = audiences | push: 'UNTITLED_EVENT' %}
{% endif %}
{% endif %}

  {% assign title = post.content | replace_first: "<br>", '
'  | strip | replace_first: '
', "<br>" | split: "<br>" | first | strip_html | truncatewords: 10 | truncate: 100 %}
  * # {{ title }}
    
    Posted by [{{ post.author.displayName }}]({{ post.author.profilePageUrl }}) on {{ post.creationTime | date_to_rfc822 }} {% if post.url contains 'https://plus.google.com/' %}[on G+]({{ post.url }}){% else %}[on {{ post.url | remove: 'https://' | remove: 'https://' | split: '/' | first }}]({{ post.url }}){% endif %}{% if post.updateTime and post.updateTime != post.creationTime %} and last updated on {{ post.updateTime | date_to_rfc822 }}{% endif %}    
    Audiences: {{ audiences | join: ', ' }}

    ---

    {% if post.media.url %}
    {% if post.media.contentType == 'image/*' %}![Media file for {{ title }} ]({{ post.media.url }}){% endif %}
    {% if post.media.contentType == 'video/*' %}<div class='embed-container'><iframe src="{{ post.media.url | replace: "http://www.youtube.com/watch?v=", "https://www.youtube.com/embed/" | replace: "https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/" | replace: "https://youtu.be/", "https://www.youtube.com/embed/" | replace: "http://youtu.be/", "https://www.youtube.com/embed/" }}" frameborder="0"></iframe></div>{% endif %}
    {% endif %}
    {% if post.album.media %}
    Found {{ post.album.media | size }} media files:
    {% for medium in post.album.media %}![Media file for {{ title }}: {{ medium.description }} ]({{ medium.url }}){% endfor %}
    {% endif %}
    {{ post.content }}

    ---

    {% if post.resharedPost %}
    {% assign title = post.resharedPost.content | replace_first: "<br>", '
'  | strip | replace_first: '
', "<br>" | split: "<br>" | first | strip_html | truncatewords: 10 | truncate: 100 %}
    * ## {{ title }}

      Posted by [{{ post.resharedPost.author.displayName }}]({{ post.resharedPost.author.profilePageUrl }}) {% if post.resharedPost.url contains 'https://plus.google.com/' %}[on G+]({{ post.resharedPost.url }}){% else %}[on {{ post.resharedPost.url | remove: 'https://' | remove: 'https://' | split: '/' | first }}]({{ post.resharedPost.url }}){% endif %}{% if post.resharedPost.updateTime and post.resharedPost.updateTime != post.resharedPost.creationTime %} and last updated on {{ post.resharedPost.updateTime | date_to_rfc822 }}{% endif %}    

      {% if post.resharedPost.media.url %}
      {% if post.resharedPost.media.contentType == 'image/*' %}![Media file for {{ title }} ]({{ post.resharedPost.media.url }}){% endif %}
      {% if post.resharedPost.media.contentType == 'video/*' %}<div class='embed-container'><iframe src="{{ post.resharedPost.media.url | replace: "http://www.youtube.com/watch?v=", "https://www.youtube.com/embed/" | replace: "https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/" | replace: "https://youtu.be/", "https://www.youtube.com/embed/" | replace: "http://youtu.be/", "https://www.youtube.com/embed/" }}" frameborder="0"></iframe></div>{% endif %}
      {% endif %}
      {% if post.resharedPost.album.media %}
      Found {{ post.resharedPost.album.media | size }} media files:
      {% for medium in post.resharedPost.album.media %}
      ![Media file for {{ title }}: {{ medium.description }} ]({{ medium.url }})
      {% endfor %}
      {% endif %}
      {{ post.resharedPost.content }}

      ---

    {% endif %}

    Original Activity ID: {{ post.activityId }}
    
    ---
    {% if page.debug == true %}
    {% highlight ruby linenos %}
    {{ post | replace: "=>{", '=>
    {' | replace: ", ", ',
      ' }}
    {% endhighlight %}
    {% endif %}

{% assign counter=counter | plus:1 %}
{% if counter >= 50 %}
{% break %}
{% endif %}
{% endfor %}

