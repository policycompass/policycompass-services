from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics, status
from django.core.exceptions import ValidationError
from .models import *
from .serializers import *
from .formula import validate_formula

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

class FormulaValidate(APIView):

    def get(self, request):
        if "formula" not in request.QUERY_PARAMS:
            return Response("No formula provided")
        try:
            validate_formula(request.QUERY_PARAMS["formula"])
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({ "formula": e.message }, status=status.HTTP_400_BAD_REQUEST)

class MetricsCreate(generics.CreateAPIView):
    model = Metric
    serializer_class = MetricSerializer

class MetricsDetail(generics.RetrieveAPIView):
    model = Metric
    serializer_class = MetricSerializer
