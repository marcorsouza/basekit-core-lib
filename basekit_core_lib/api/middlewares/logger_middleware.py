from datetime import datetime
import functools

from flask import Response, request
from config.helpers import logger

def log_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Executing method: {func.__name__}")
            
            start_time = datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.now()
            
            execution_time = end_time - start_time
            logger.info(f"Method execution time: {execution_time.total_seconds()} seconds")
            
            if isinstance(result, Response):
                status_code = result.status_code
                
                # Tratamento de status code específico
                if status_code == 404:
                    logger.warning(f"Resource not found: {request.path}")
                elif status_code == 503:
                    logger.error("Service unavailable")
                elif status_code >= 500:
                    logger.error("Server error")
                elif status_code == 400:
                    logger.error("Bad request")
                elif status_code == 401:
                    logger.error("Unauthorized")
                elif status_code == 403:
                    logger.error("Forbidden")
                
            logger.info(f"Finished executing method: {func.__name__}")
            
            return result
        return wrapper