import time

class TimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start
        print(f'View {request.path} took {duration:.2f}')

        return response


from django.utils.cache import patch_cache_control
from django.utils.deprecation import MiddlewareMixin


class AnonymousCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            patch_cache_control(response, no_cache = True, private = True)

        else:
            patch_cache_control(response, public = True)
        return response

        
        