"""
Mocking of a User Management API
DEPRECATED
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import AuthSerializer

class UserAuth(APIView):

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = AuthSerializer(data=data)
        if serializer.is_valid():
            result = {'token': serializer.user.token}
            return Response(result)
        else:
            return Response(serializer.errors, status=400)


