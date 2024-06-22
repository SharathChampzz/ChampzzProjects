import logging
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('WebServer')

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info(f'{request.method} {request.get_full_path()} {request.body.decode() if request.body else ""}')
        request.start_time = time.time()
    
    def process_response(self, request, response):
        duration = time.time() - request.start_time
        logger.info(f'{request.method} {request.get_full_path()} {response.status_code} {duration:.2f}s')
        return response
