from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from basekit_core_lib.config.config import ConfigFactory, Config
from basekit_core_lib.config.loggers import Logger

db : SQLAlchemy = SQLAlchemy()
ma : Marshmallow = Marshmallow()

config : Config = ConfigFactory.get_config()
logger : Logger= Logger(config)