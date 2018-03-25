from flask import Blueprint

from core.core_app import CoreApp


def create_app(config=None):
    """
    Build the app build don't initialize it, useful to get back the default
    app config, correct it, then call ``bootstrap_app`` with the new config
    """
    app = CoreApp(__name__)

    if config:
        app.config.update(config)
    app.config.from_pyfile('default_settings.cfg')

    return app


def bootstrap_app(app=None, config=None):
    """
    Create and initialize the app
    """

    if not app:
        app = create_app(config)
    elif config:
        app.config.update(config)

    app.bootstrap()

    from blog.view import api

    # view.prefix = app.config['BACKEND_PREFIX']
    # app.init_app(app)

    blueprint = Blueprint('view', __name__, url_prefix=app.config['BACKEND_PREFIX'])
    api.init_app(blueprint)

    # view.add_namespace(posts_namespace)
    # view.add_namespace(category_namespace)

    app.register_blueprint(blueprint)

    return app
