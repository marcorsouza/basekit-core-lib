from functools import wraps
import inspect
from flask import jsonify
from config.helpers import logger

def handle_exceptions(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = str(e)
            logger.error(error_message)
            response = {'error': error_message}
            return jsonify(response), 500

    return wrapper