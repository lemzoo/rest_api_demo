import logging

from flask import request
from flask_restplus import Resource, Api, fields

from blog.api.blog.business import CategoryRepository


log = logging.getLogger(__name__)

api = Api(version='1.0', title='Blog''s Categories',
          description='A simple demonstration of a Flask RestPlus powered API')

ns = api.namespace('blog/categories', description='Operations related to blog categories')


category = api.model('Blog category', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a blog category'),
    'name': fields.String(required=True, description='Category name'),
    'status': fields.String(description='Status of the category'),
    'created_at': fields.DateTime(description='Creation date of the category'),
    'updated_at': fields.DateTime(description='Date where the category is updated'),
    'deleted_at': fields.DateTime(description='Date where the category is deleted')
})


category_with_posts = api.inherit('Blog category with posts', category, {
    # 'posts': fields.List(category)
})


@ns.route('/')
class CategoryCollection(Resource):

    @api.marshal_list_with(category)
    def get(self):
        """
        Returns list of blog categories.
        """
        return CategoryRepository.get_all()

    @api.response(201, 'Category successfully created.')
    @api.expect(category)
    def post(self):
        """
        Creates a new blog category.
        """
        payload = request.json
        CategoryRepository.create(payload)

        return None, 201


@ns.route('/<int:category_id>')
@api.response(404, 'Category not found.')
class CategoryItem(Resource):

    @api.marshal_with(category_with_posts)
    def get(self, category_id):
        """
        Returns a category with a list of posts.
        """
        category_gotten = CategoryRepository.get_by_id(id=category_id)
        return category_gotten

    @api.expect(category)
    @api.response(204, 'Category successfully updated.')
    def put(self, category_id):
        """
        Updates a blog category.

        Use this method to change the name of a blog category.

        * Send a JSON object with the new name in the request body.

        ```
        {
          "name": "New Category Name"
        }
        ```

        * Specify the ID of the category to modify in the request URL path.
        """
        payload = request.json
        CategoryRepository.update(category_id, payload)

        return None, 204

    @api.response(204, 'Category successfully deleted.')
    def delete(self, category_id):
        """
        Deletes blog category.
        """
        CategoryRepository.soft_delete(category_id)

        return None, 204
