import logging
import traceback

from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound

from blog.api.blog.endpoints.categories import ns as category_namespace


log = logging.getLogger(__name__)

api = Api(version='1.0', title='My Blog API',
          description='A simple demonstration of a Flask RestPlus powered API')

api.add_namespace(category_namespace)


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A model result was required but none was found.'}, 404
