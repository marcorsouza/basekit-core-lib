from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config.config import ConfigFactory, Config
from config.loggers import Logger

db : SQLAlchemy = SQLAlchemy()
ma : Marshmallow = Marshmallow()

config : Config = ConfigFactory.get_config()
logger : Logger= Logger(config)