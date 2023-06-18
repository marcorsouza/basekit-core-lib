from basekit_core_lib.api.routes.login_routes import login_routes
def add_login_route(blueprint):
    blueprint.register_blueprint(login_routes)