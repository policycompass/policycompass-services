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
Compute a new dataset from a given formula and mappings for variables.

Example data:

  {
    "datasets": [
      {
        "variable": "__1__",
        "dataset": 1
      }
    ]
  }


"""
class MetriscOperationalize(APIView):

    def _get_dataset(self, dataset_id: int):
        from apps.datasetmanager.models import Dataset
        from apps.datasetmanager.dataset_data import DatasetData
        dataset = Dataset.objects.get(pk=dataset_id)
        dataset.data = DatasetData.from_json(dataset.data)
        return dataset

    def _store_dataset(self, dataset):
        dataset.data = dataset.data.to_json
        dataset.save()
        return dataset.id

    def post(self, request, pk: int):
        # check if metric exists
        metric = Metric.objects.get(pk=pk)
        if Metric.objects.get(pk=pk) is None:
            return Response("Unable to find metric %s." % pk, status=status.HTTP_404_NOT_FOUND)

        # check resquest data
        serializer = OperationalizeSerializer(data=request.DATA, files=request.FILES)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # load required data sets
        id_mapping = serializer.object
        mapping = { variable: self._get_dataset(dataset_id) for (variable, dataset_id) in id_mapping.items() }

        # normalize time slots (extract data frame)


        # compute result
        formula = metric.formula
        result = compute_formula(formula, mapping)

        # store dataset
        print(mapping)
        print(result)
        # TODO: create dataset here
        dataset_id = 1

        return Response({
            "dataset": {
                "id":  dataset_id
            }
        })
