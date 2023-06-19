from basekit_core_lib.utils.file_utils import get_env, get_key_generator
import os
class Config:
    
    SECRET_KEY = get_env('SECRET_KEY', get_key_generator(32))

    DEBUG = get_env('DEBUG', False)
    TESTING = get_env('TESTING', False)
    HOST = get_env('DSV_HOST', '0.0.0.0')
    PORT = get_env('DSV_PORT', 5000)

    LOG_LEVEL = get_env('LOG_LEVEL', 'DEBUG')
    LOG_MAX_SIZE = int(get_env('LOG_MAX_SIZE', 1048576))
    LOG_BACKUP_COUNT = int(get_env('LOG_BACKUP_COUNT', 50))
    LOG_TO_CONSOLE = get_env('LOG_TO_CONSOLE', False)

    SQLALCHEMY_DATABASE_URI = get_env('DSV_DATABASE_URI', 'mysql://root@localhost/meudb')
    SQLALCHEMY_TRACK_MODIFICATIONS = get_env('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    APPLICATION_ACRONYM = get_env('APPLICATION_ACRONYM', None)
    LOG_FOLDER = get_env('LOG_FOLDER', 'logs')
    APPLICATION_FOLDER = get_env('APPLICATION_FOLDER', 'basekit')
    API_FOLDER = get_env('API_FOLDER', 'api')

    EXPIRE_TOKEN = int(get_env('EXPIRE_TOKEN', 60))
    EXPIRE_REFRESH_TOKEN = int(get_env('EXPIRE_REFRESH_TOKEN', 30))
    TEMPORARY_PASSWORD_EXPIRATION = int(get_env('TEMPORARY_PASSWORD_EXPIRATION', 8))
    API_AUTH_URL = get_env('API_AUTH_URL', 'http://127.0.0.1:5000/api/auth')

class DevelopmentConfig(Config):
    SECRET_KEY = get_env('SECRET_KEY', os.urandom(32))
    
    DEBUG = False
    TESTING = False
    HOST = get_env('DSV_HOST', "0.0.0.0")
    PORT = get_env('DSV_PORT', 3000)
    
    LOG_LEVEL=get_env('LOG_LEVEL', "DEBUG")
    LOG_MAX_SIZE = int(get_env('LOG_MAX_SIZE', 1048576))
    LOG_BACKUP_COUNT = int(get_env('LOG_BACKUP_COUNT', 50))
    LOG_TO_CONSOLE = get_env('LOG_TO_CONSOLE', False)
    
    SQLALCHEMY_DATABASE_URI = get_env('DSV_DATABASE_URI', 'mysql://root@localhost/meudb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class ProductionConfig(Config):
    SECRET_KEY = get_env('SECRET_KEY', os.urandom(32))
    
    DEBUG = False
    TESTING = False
    HOST = get_env('PRD_HOST', "0.0.0.0")
    PORT = get_env('PRD_PORT', 5000)
    
    LOG_LEVEL=get_env('LOG_LEVEL', "DEBUG")
    LOG_MAX_SIZE = int(get_env('LOG_MAX_SIZE', 1048576))
    LOG_BACKUP_COUNT = int(get_env('LOG_BACKUP_COUNT', 50))
    LOG_TO_CONSOLE = get_env('LOG_TO_CONSOLE', True)
    
    SQLALCHEMY_DATABASE_URI = get_env('PRD_DATABASE_URI', 'mysql://root@localhost/meudb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class TestingConfig(Config):
    SECRET_KEY = get_env('SECRET_KEY', os.urandom(32))
    
    DEBUG = False
    TESTING = False
    HOST = get_env('HML_HOST', "0.0.0.0")
    PORT = get_env('HML_PORT', 4000)
    
    LOG_LEVEL=get_env('LOG_LEVEL', "DEBUG")
    
    SQLALCHEMY_DATABASE_URI = get_env('HML_DATABASE_URI', 'mysql://root@localhost/meudb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
        
class ConfigFactory:
    @staticmethod
    def get_config():
        env = get_env('FLASK_ENV', 'development')
        if env == 'production':
            return ProductionConfig()
        elif env == 'testing':
            return TestingConfig()
        else:
            return DevelopmentConfig()