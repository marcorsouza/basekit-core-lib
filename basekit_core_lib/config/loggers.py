import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        log_level = logging.DEBUG

        if config.LOG_LEVEL == "DEBUG":
            log_level = logging.DEBUG
        elif config.LOG_LEVEL == "INFO":
            log_level = logging.INFO
        elif config.LOG_LEVEL == "ERROR":
            log_level = logging.ERROR
            
        self.logger.setLevel(log_level)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_folder = config.LOG_FOLDER
        
        now = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(log_folder, f"{now}.log")
        os.makedirs(log_folder, exist_ok=True)
        
        self.handler = RotatingFileHandler(log_file, maxBytes=config.LOG_MAX_SIZE, backupCount=config.LOG_BACKUP_COUNT)
        self.handler.setLevel(log_level)
        self.handler.setFormatter(formatter)
        
        self.logger.addHandler(self.handler)
        
        if config.LOG_TO_CONSOLE:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(console_handler)
            
    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def _get_log_level(self, level):
        level = level.upper()
        if level == "DEBUG":
            return logging.DEBUG
        elif level == "INFO":
            return logging.INFO
        elif level == "ERROR":
            return logging.ERROR
        else:
            return logging.WARNING

