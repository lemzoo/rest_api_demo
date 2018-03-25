import logging

from flask import request
from flask_restplus import Resource
from blog.api.blog.business import PostRepository # create_blog_post, update_post, delete_post
from blog.api.blog.serializers import blog_post, page_of_blog_posts
from blog.api.blog.parsers import pagination_arguments
from blog.api.restplus import api
from blog.model.models import Post

log = logging.getLogger(__name__)

ns = api.namespace('blog/posts', description='Operations related to blog posts')


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
