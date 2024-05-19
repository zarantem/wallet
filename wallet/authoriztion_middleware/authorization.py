from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.exceptions import APIException
from rest_framework.request import Request


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION', None)

        if jwt_token:
            try:
                _, user = JSONWebTokenAuthentication().authenticate(Request(request))
                request.user = user
            except APIException as e:
                pass

        response = self.get_response(request)
        return response
