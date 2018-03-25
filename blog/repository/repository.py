from datetime import datetime

from flask import current_app

from blog.model.models import Post, Category


class PostRepository:

    @staticmethod
    def get_all(page, per_page):
        current_session = current_app.session
        return current_session.query(Post).all()

    @staticmethod
    def get_by_id(id):
        current_session = current_app.session
        post = current_session.query(Post).filter_by(id=id).first()

        return post

    @staticmethod
    def create(payload):
        title = payload.get('title')
        body = payload.get('body')
        category_id = payload.get('category_id')

        category = CategoryRepository.get_by_id(category_id)

        current_session = current_app.session

        post = Post(title=title, body=body, category_id=category.id)

        current_session.add(post)
        current_session.commit()

    @classmethod
    def update(cls, id, payload):

        post = cls.get_by_id(id)
        post.title = payload.get('title')
        post.body = payload.get('body')
        post.category_id = payload.get('category_id')
        post.status = 'updated'

        current_session = current_app.session.object_session(post)
        current_session.add(post)
        current_session.commit()

    @classmethod
    def soft_delete(cls, post_id):
        post = cls.get_by_id(post_id)
        post.status = 'deleted'
        post.deleted_at = datetime.utcnow()

        current_session = current_app.session.object_session(post)
        current_session.add(post)
        current_session.commit()


class CategoryRepository:

    @staticmethod
    def get_all():
        current_session = current_app.session
        return current_session.query(Category).all()

    @staticmethod
    def get_by_id(id):
        current_session = current_app.session
        category = current_session.query(Category).filter_by(id=id).first()

        return category

    @staticmethod
    def create(paylaod):
        current_session = current_app.session

        name = paylaod.get('name')
        category = Category(name=name)

        current_session.add(category)
        current_session.commit()

    @classmethod
    def update(cls, category_id, payload):
        category = cls.get_by_id(category_id)
        category.name = payload.get('name')
        category.status = 'updated'

        current_session = current_app.session.object_session(category)
        current_session.add(category)
        current_session.commit()

    @classmethod
    def soft_delete(cls, category_id):
        category = cls.get_by_id(category_id)
        category.status = 'deleted'
        category.deleted_at = datetime.utcnow()

        current_session = current_app.session.object_session(category)
        current_session.add(category)
        current_session.commit()
