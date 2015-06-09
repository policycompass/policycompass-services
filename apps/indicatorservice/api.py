__author__ = 'fki'

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.reverse import reverse
from rest_framework import viewsets


class IndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = IndicatorSerializer
    queryset = Indicator.objects.all()

    # def get_queryset(self):
    #
    #     queryset = Individual.objects.all()
    #     data_class = self.request.QUERY_PARAMS.get('class', None)
    #     if data_class is not None:
    #         try:
    #             data_class = int(data_class)
    #             queryset = queryset.filter(data_class__id=data_class)
    #         except ValueError:
    #             queryset = queryset.filter(data_class__title=data_class)
    #     return queryset


