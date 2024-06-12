from threading import local

_request = local()


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request.value = request
        response = self.get_response(request)
        _request.value = None
        return response


def get_current_request():
    return _request.value


def get_current_user():
    request = get_current_request()
    if request:
        return request.user
    else:
        return None


def get_current_ip():
    request = get_current_request()
    if request:
        return request.META.get('REMOTE_ADDR')
    else:
        return None


def get_current_user_agent():
    request = get_current_request()
    if request:
        return request.META.get('HTTP_USER_AGENT')
    else:
        return None
