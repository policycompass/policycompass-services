__author__ = 'fki'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics
from .models import *
from .serializers import *


class Base(APIView):

    def get(self, request):
        """
        :type request: Request
        :param request:
        :return:
        """
        response = "Not yet implemented."
        return Response(response)


class DatasetList(generics.ListCreateAPIView):
    model = Dataset
    serializer_class = DatasetSerializer


class DatasetDetail(generics.RetrieveUpdateDestroyAPIView):

    model = Dataset
    serializer_class = DatasetSerializer