from sqlalchemy.exc import IntegrityError
from flask import request, jsonify, make_response
import inspect
from abc import ABC

from api.middlewares.logger_middleware import log_decorator
from config.helpers import logger

class BaseController(ABC):
    def __init__(self, service):
        self.service = service        
            
    @log_decorator
    def get_all(self):
        try:
            data = self.service.get_all()
            logger.info("get_all successful")
            return self.build_success_response(data)
        except Exception as e:
            logger.error("get_all error: %s", str(e))
            return self.build_error_response(str(e), 500)
    
    @log_decorator
    def get_by_id(self, id):
        try:
            data = self.service.get_by_id(id)
            if data:
                logger.info("get_by_id successful")
                return self.build_success_response(data)
            else:
                logger.error("get_by_id error: Object with id %s not found", id)
                return self.build_error_response(f"Object with id {id} not found", 404)
        except Exception as e:
            logger.error("get_by_id error: %s", str(e))
            return self.build_error_response(str(e), 500)
    
    @log_decorator
    def create(self):
        try:
            data = request.get_json()
            obj = self.service.create(data)
            logger.info("create successful")
            return self.build_success_response(obj, 201)
        except IntegrityError as e:
            logger.error("create error: Integrity error")
            return self.build_error_response("Integrity error", 400)
        except Exception as e:
            logger.error("create error: %s", str(e))
            return self.build_error_response(str(e), 500)
    
    @log_decorator
    def update(self, id):
        try:
            data = request.get_json()
            obj = self.service.update(id, data)
            if obj:
                logger.info("update successful")
                return self.build_success_response(obj)
            else:
                logger.error("update error: Object with id %s not found", id)
                return self.build_error_response(f"Object with id {id} not found", 404)
        except IntegrityError as e:
            logger.error("update error: Integrity error")
            return self.build_error_response("Integrity error", 400)
        except Exception as e:
            logger.error("update error: %s", str(e))
            return self.build_error_response(str(e), 500)
    
    @log_decorator
    def delete(self, id):
        try:
            success = self.service.delete(id)
            if success:
                logger.info("delete successful")
                return self.build_success_response({"message": "Object deleted successfully"})
            else:
                logger.error("delete error: Object with id %s not found", id)
                return self.build_error_response(f"Object with id {id} not found", 404)
        except Exception as e:
            logger.error("delete error: %s", str(e))
            return self.build_error_response(str(e), 500)
    
    def build_success_response(self, data, status_code=200):
        return make_response(jsonify({"success": True, "data": data}), status_code)
    
    def build_error_response(self, error_message, status_code):
        return make_response(jsonify({"success": False, "error": error_message}), status_code)
