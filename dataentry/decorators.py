from django.views.decorators.cache import cache_page
from functools import wraps


def cache_for_anonymous(timeout):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            return cache_page(timeout)(view_func)(request, *args, **kwargs )
        return wrapped_view
    return decorator
            