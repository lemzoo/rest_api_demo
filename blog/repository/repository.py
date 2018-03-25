from datetime import datetime

from flask import current_app

from blog.model.models import Post, Category


class PostRepository:

    @staticmethod
    def get_by_id(id):
        current_session = current_app.session
        return current_session.query(Post).filter_by(id=id)

    @staticmethod
    def create(post):
        current_session = current_app.session
        current_session.add(post)
        current_session.commit()

    @staticmethod
    def update(post):
        current_session = current_app.session
        current_session.add(post)
        current_session.commit()

    @classmethod
    def soft_delete(cls, post):
        post.status = 'deleted'
        post.deleted_at = datetime.utcnow()
        cls.update(post)


class CategoryRepository:
    @staticmethod
    def get_by_id(id):
        current_session = current_app.session
        return current_session.query(Category).filter_by(id=id)

    @staticmethod
    def create(category):
        current_session = current_app.session
        current_session.add(category)
        current_session.commit()

    @staticmethod
    def update(category):
        current_session = current_app.session
        current_session.add(category)
        current_session.commit()

    @classmethod
    def soft_delete(cls, category):
        category.status = 'deleted'
        category.deleted_at = datetime.utcnow()
        cls.update(category)
