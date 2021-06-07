import asyncio
from django.utils.deprecation import MiddlewareMixin

from authentication.controller_access_ips import control

loop = asyncio.new_event_loop()


class ControlAccessMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response=get_response)
        self.get_response = get_response

    def process_request(self, request):
        ip = request.META['REMOTE_ADDR']
        if ip != '127.0.0.1':
            loop.run_in_executor(None, control, ip)
