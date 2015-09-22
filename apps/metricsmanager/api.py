from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics, status
from django.core.exceptions import ValidationError
from .models import *
from .serializers import *
from .formula import validate_formula, compute_formula

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
            return Response({ "formula": "Can not be empty"}, status=status.HTTP_400_BAD_REQUEST)
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


"""

Example data:

{
  "datasets": [
    { "variable": "__1__", "dataset": 1 }
  ]
}


"""
class MetriscOperationalize(APIView):
    def post(self, request, pk):
        # check if metric exists
        metric = Metric.objects.get(pk=pk)
        if Metric.objects.get(pk=pk) is None:
            return Response("Unable to find metric %s." % pk, status=status.HTTP_404_NOT_FOUND)

        # check resquest data
        serializer = OperationalizeSerializer(data=request.DATA, files=request.FILES)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # load required data sets

        # compute result
        mapping = serializer.object
        formula = metric.formula
        result = compute_formula(formula, mapping)

        # store dataset
        dataset_id = 1

        return Response({
            "dataset": {
                "id": dataset_id
            }
        })
