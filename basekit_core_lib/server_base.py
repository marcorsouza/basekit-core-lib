import inspect
import os
from flask import Blueprint, Flask
from flask_jwt_extended import JWTManager
from basekit_core_lib.config.helpers import db, ma, config
from basekit_core_lib.api.middlewares.auth_middleware import authenticate
from basekit_core_lib.api.routes.login_routes import login_routes
from abc import ABC, abstractmethod

class ServerBase(ABC):
    def __init__(self, app: Flask) -> None:
        self.app = app
        self.blue_print = Blueprint('api', __name__, url_prefix='/api')           
        self.config =config
        self.app.config.from_object(self.config)
        
        self.app.secret_key = self.config.SECRET_KEY
        self.app.config['JWT_SECRET_KEY'] = self.config.SECRET_KEY # Defina sua chave secreta
        JWTManager(self.app)
                
        self.configure_routes()
        self.blue_print.register_blueprint(login_routes)
        self.app.register_blueprint(self.blue_print)
        db.init_app(self.app)
        ma.init_app(self.app)
        self.swagger_init_app()
        
        self.configure_autenticate_routes()
        
        super().__init__()
    
    @abstractmethod 
    def configure_routes(self):            
        pass
    
    @abstractmethod
    def swagger_init_app(self):
        pass
        
    def configure_autenticate_routes(self,):
        for route in self.app.url_map.iter_rules():
            if route.rule.startswith('/api/') and not route.rule.startswith('/api/auth/') and not 'recovery_password' in route.rule:
                self.app.view_functions[route.endpoint] = authenticate(self.app.view_functions[route.endpoint])
            
    def run(self, ):
        self.app.run(
            port=self.config.PORT,
            debug=self.config.DEBUG,
            host=self.config.HOST
        )