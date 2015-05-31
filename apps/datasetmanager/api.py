__author__ = 'fki'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request


class Base(APIView):

    def get(self, request):
        """
        :type request: Request
        :param request:
        :return:
        """
        response = "Not yet implemented."
        return Response(response)

