from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from basekit_core_lib.config.config import ConfigFactory, Config
from basekit_core_lib.config.loggers import Logger

try:
    db: SQLAlchemy = SQLAlchemy()
except Exception as e:
    print("Falha ao criar objeto 'db'. Erro: ", str(e))

try:
    ma: Marshmallow = Marshmallow()
except Exception as e:
    print("Falha ao criar objeto 'ma'. Erro: ", str(e))

try:
    config: Config = ConfigFactory.get_config()
except Exception as e:
    print("Falha ao criar objeto 'config'. Erro: ", str(e))

try:
    logger: Logger = Logger(config)
except Exception as e:
    print("Falha ao criar objeto 'logger'. Erro: ", str(e))