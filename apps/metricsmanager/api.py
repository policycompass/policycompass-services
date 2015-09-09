from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics
from .models import *
from .serializers import *

class MetricsBase(APIView):

    def get(self, request, format=None):
        """
        :type request: Request
        :param request:
        :return:
        """
        result = {
            "Metrics": reverse('metrics-create', request=request)
        }

        return Response(result)

class MetricsCreate(generics.CreateAPIView):
    model = Metric
    serializer_class = MetricSerializer

class MetricsDetail(generics.RetrieveAPIView):
    model = Metric
    serializer_class = MetricSerializer
