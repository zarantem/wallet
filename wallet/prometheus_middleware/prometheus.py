from prometheus_client import start_http_server, Summary
from django.utils.deprecation import MiddlewareMixin

# Счетчики и сумматоры для Prometheus
request_processing_time = Summary('request_processing_seconds', 'Time spent processing request')

class PrometheusMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        self.get_response = get_response
        start_http_server(8000)  # Начать HTTP сервер для экспозиции метрик Prometheus

    def process_request(self, request):
        self.start_time = time.time()

    def process_response(self, request, response):
        request_processing_time.observe(time.time() - self.start_time)
        return response
