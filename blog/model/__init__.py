from flask_sqlalchemy import SQLAlchemy

from blog.model.models import BaseModel

db = SQLAlchemy()


def reset_database():
    # from blog.model.models import Post, Category  # noqa
    db.drop_all()
    db.create_all()


def create_schema(app):
    BaseModel.metadata.create_all(app.engine)
