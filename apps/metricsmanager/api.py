from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics, status
from django.core.exceptions import ValidationError
from apps.datasetmanager.models import Dataset
from apps.datasetmanager.dataset_data import DatasetData
from .models import *
from .serializers import *
from .formula import validate_formula, compute_formula
import itertools
from datetime import datetime

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
    "title" : "Some test",
    "acronym": "acronym",
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

    def _filter_dataset(self, **kwargs):
        from apps.datasetmanager.models import Dataset
        from apps.datasetmanager.dataset_data import DatasetData
        datasets = Dataset.objects.filter(**kwargs)
        for dataset in datasets:
            dataset.data = DatasetData.from_json(dataset.data)
        return datasets

    def _store_dataset(self, dataset):
        dataset.data = dataset.data.get_json()
        dataset.save()
        return dataset.id

    def post(self, request, metrics_id: int):
        # check if metric exists
        metric = Metric.objects.get(pk=metrics_id)
        if Metric.objects.get(pk=metrics_id) is None:
            return Response("Unable to find metric %s." % pk, status=status.HTTP_404_NOT_FOUND)

        # check resquest data
        serializer = OperationalizeSerializer(data=request.DATA, files=request.FILES)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # check if dateset with that title and acronym already existed
        title = serializer.object.get("title")
        acronym = serializer.object.get("acronym")
        error = {}
        if len(self._filter_dataset(title = title)) != 0:
            error["title"] = "Dataset name is not unique."
        if len(self._filter_dataset(acronym = acronym)) != 0:
            error["acronym"] = "Dataset acronym is not unique."
        if len(error) != 0:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        # load required data sets
        id_mapping = serializer.object.get("datasets")
        mapping = { variable: self._get_dataset(dataset_id) for (variable, dataset_id) in id_mapping.items() }

        # normalize time resolution (and extract data frame)
        result_time_resolution = "year"
        result_time_start = "2001"
        result_time_end = "2009"
        result_unit = 0

        # compute result
        result = compute_formula(metric.formula, mapping)

        # dataset
        data = DatasetData(
            data_frame = result,
            unit = result_unit,
            resolution = result_time_resolution)

        dataset = Dataset(
            title = title,
            acronym = acronym,
            description = "Computed formular '%s' with %s" % (
                metric.formula,
                ", ".join([ "'%s' as %s" % (dataset.title, variable) for variable, dataset in mapping.items()])),
            keywords = ", ".join(set(itertools.chain([ dataset.keywords for dataset in mapping.values()]))),
            version = 0,
            # ressource related info
            resource_url = reverse("metrics-detail", kwargs={'pk': metrics_id}),
            resource_issued = datetime.now(),
            # metrics identifier
            is_applied = True,
            metric_id = metrics_id,
            # contained data
            time_resolution = result_time_resolution,
            time_start = result_time_start,
            time_end = result_time_end,
            data = data,
            # references to other services
            # TODO add useful values here
            language_id = 0,
            user_id = 0,
            unit_id = result_unit,
            indicator_id = metric.indicator,
            class_id = 0)

        dataset_id = self._store_dataset(dataset)

        return Response({
            "dataset": {
                "id":  dataset_id
            }
        })
