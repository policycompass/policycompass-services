from rest_framework import authentication
from rest_framework import exceptions, HTTP_HEADER_ENCODING
from rest_framework.authentication import get_authorization_header
import logging as log

class User(object):

    def __init__(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def is_authenticated(self):
        return True

    def __str__(self):
        return "User " + str(self.__id)


class PolicyCompassAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = self.__get_token(request)
        if token:
            return User(token), None
        else:
            return None

    def __get_token(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)

        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]






