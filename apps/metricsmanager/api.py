from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Metric, Unit
from .serializers import WriteMetricSerializer, ReadMetricSerializer, ListMetricSerializer, UnitSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthenticatedCanCreate
from .utils import get_rawdata_for_metric
from django.db import IntegrityError, transaction


import logging
log = logging.getLogger(__name__)


class MetricList(APIView):
    #permission_classes = (IsAuthenticatedCanCreate,)
    model = Metric

    def options(self, request, *args, **kwargs):
        return Response("Options")

    def get(self, request):
        metrics = Metric.objects.all()
        serializer = ReadMetricSerializer(metrics, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = WriteMetricSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            log.info(serializer.object)
            s = ReadMetricSerializer(serializer.object)
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MetricDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Metric
    serializer_class = ReadMetricSerializer


class UnitList(generics.ListAPIView):
    model = Unit
    serializer_class = UnitSerializer


class UnitDetail(generics.RetrieveAPIView):
    model = Unit
    serializer_class = UnitSerializer