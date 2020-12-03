# Declare module of your plugin under Jekyll module
module Jekyll::CustomFilter

	def public_posts_filter(posts)
		# selected_posts = []
		# posts.select do |post|
		# 	users = post['postAcl']['collectionAcl']['users']
		# 	return false if users.nil? || post['postAcl']['collectionAcl']['users'].empty?
		# 	users.any? do |user|
		# 		userid = user['resourceName'].split("/").last
		# 		!post['content'].include?(userid) && !_userid_in_comments(userid, post['comments'])
		# 	end
		# end
		posts
  end

	def reshared_posts_filter(posts)
		# and post.postAcl.collectionAcl and post.postAcl.collectionAcl.users.size > 0
		selected_posts = []
		posts.select do |post|
			users = post['postAcl']['collectionAcl']['users']
			return false if users.nil? || post['postAcl']['collectionAcl']['users'].empty?
			users.any? do |user|
				userid = user['resourceName'].split("/").last
				!post['content'].include?(userid) && !_userid_in_comments(userid, post['comments'])
			end
		end
  end

	private

	def _userid_in_comments(userid, comments)
		return false if comments.nil?
		comments.any? do |comment|
			comment['content'].include?(userid)
		end
	end
end

Liquid::Template.register_filter(Jekyll::CustomFilter)
