from os.path import abspath, dirname

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class CoreApp(Flask):
    """
    CoreApp is a regular :class:`Flask` app
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root_path = abspath(dirname(__file__))
        self.engine = None

    def bootstrap(self):
        url = self.config['POSTGRES_URL']
        self.engine = create_engine(url)

    @property
    def session(self):
        Session = sessionmaker(autoflush=False, bind=self.engine)
        session = Session(autocommit=False)
        return session
