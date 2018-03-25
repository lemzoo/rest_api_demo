from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


BaseModel = declarative_base()


class Post(BaseModel):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(80))
    body = Column(Text)
    status = Column(String(20), default='available')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    category_id = Column(Integer, ForeignKey('category.id'))

    def __repr__(self):
        return 'Post<{title}, {body}, {status}>'.format(title=self.title,
                                                        body=self.body,
                                                        status=self.status)


class Category(BaseModel):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    status = Column(String(20), default='available')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return '<Category {name}, {status}>'.format(name=self.name, status=self.status)
