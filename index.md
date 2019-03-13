---
layout: home
---
{% for post_h in site.data.posts %}
{% assign gpost = post_h[1] %}
  * #{{ gpost.activityId }}: [{{ gpost.url }}]({{ gpost.url }})
{% endfor %}