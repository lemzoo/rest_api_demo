import logging

from flask import request
from flask_restplus import reqparse, fields, Resource

from blog.view.__init__ import api

from blog.model.models import Post

from blog.repository.repository import PostRepository


log = logging.getLogger(__name__)

ns = api.namespace('blog/posts', description='Operations related to blog posts')


pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page {error_msg}')


blog_post = api.model('Blog post', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a blog post'),
    'title': fields.String(required=True, description='Article title'),
    'body': fields.String(required=True, description='Article content'),
    'status': fields.String(required=False, description='Status of the article content'),
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'deleted_at': fields.DateTime,
    'category_id': fields.Integer,
})


pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})


page_of_blog_posts = api.inherit('Page of blog posts', pagination, {
    'items': fields.List(fields.Nested(blog_post))
})


@ns.route('')
class PostsAPI(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_list_with(blog_post)
    def get(self):
        """
        Returns list of blog posts.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        posts = PostRepository.get_all(page, per_page)

        return posts

    @api.expect(blog_post)
    def post(self):
        """
        Creates a new blog post.
        """
        payload = request.json
        new_post = PostRepository.create(payload)

        return new_post.id, 201


@ns.route('/<int:post_id>')
@api.response(404, 'Post not found.')
class PostItem(Resource):

    @api.marshal_with(blog_post)
    def get(self, post_id):
        """
        Returns a blog post.
        """
        return PostRepository.get_by_id(id=post_id)

    @api.expect(blog_post)
    @api.response(204, 'Post successfully updated.')
    def put(self, post_id):
        """
        Updates a blog post.
        """
        payload = request.json
        PostRepository.update(post_id, payload)
        return None, 204

    @api.response(204, 'Post successfully deleted.')
    def delete(self, post_id):
        """
        Deletes blog post.
        """
        PostRepository.soft_delete(post_id)
        return None, 204


@ns.route('/archive/<int:year>/')
@ns.route('/archive/<int:year>/<int:month>/')
@ns.route('/archive/<int:year>/<int:month>/<int:day>/')
class PostsArchiveCollection(Resource):

    @api.expect(pagination_arguments, validate=True)
    @api.marshal_with(page_of_blog_posts)
    def get(self, year, month=None, day=None):
        """
        Returns list of blog posts from a specified time period.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        start_month = month if month else 1
        end_month = month if month else 12
        start_day = day if day else 1
        end_day = day + 1 if day else 31
        start_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, start_month, start_day)
        end_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, end_month, end_day)
        posts_query = Post.query.filter(Post.pub_date >= start_date).filter(Post.pub_date <= end_date)

        posts_page = posts_query.paginate(page, per_page, error_out=False)

        return posts_page
