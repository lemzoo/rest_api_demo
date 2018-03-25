from flask_restplus import fields
# from blog.api.restplus import api


# blog_post = api.model('Blog post', {
#     'id': fields.Integer(readOnly=True, description='The unique identifier of a blog post'),
#     'title': fields.String(required=True, description='Article title'),
#     'body': fields.String(required=True, description='Article content'),
#     'status': fields.String(required=False, description='Status of the article content'),
#     'created_at': fields.DateTime,
#     'updated_at': fields.DateTime,
#     'deleted_at': fields.DateTime,
#     'category_id': fields.Integer,
# })
#
#
# pagination = api.model('A page of results', {
#     'page': fields.Integer(description='Number of this page of results'),
#     'pages': fields.Integer(description='Total number of pages of results'),
#     'per_page': fields.Integer(description='Number of items per page of results'),
#     'total': fields.Integer(description='Total number of results'),
# })
#
#
# page_of_blog_posts = api.inherit('Page of blog posts', pagination, {
#     'items': fields.List(fields.Nested(blog_post))
# })

