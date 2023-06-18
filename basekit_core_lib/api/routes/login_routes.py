from basekit_core_lib.api.middlewares.exception_middleware import handle_exceptions
from basekit_core_lib.api.middlewares.auth_middleware import login
from flask import Blueprint, request


login_routes = Blueprint('login_routes', __name__, url_prefix='auth')

@login_routes.route('/do_login', methods=['POST'])
@handle_exceptions
def do_login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    return login(username, password)