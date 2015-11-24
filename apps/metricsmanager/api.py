from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, status
from django.core.exceptions import ValidationError
from apps.datasetmanager import internal_api as datasets
from apps.datasetmanager.models import Dataset
from apps.datasetmanager.dataset_data import DatasetData
from .serializers import *
from .normalization import get_normalizers
from .formula import validate_variables, validate_formula, compute_formula
import itertools
import json
from datetime import datetime


class MetricsBase(APIView):
    def get(self, request, format=None):
        """
        :type request: Request
        :param request:
        :return:
        """
        result = {
            "Metrics": reverse('metrics-create-list', request=request),
            "Normalizer": reverse('normalizers-list', request=request),
        }

        return Response(result)


class FormulasValidate(APIView):
    def get(self, request):
        if "formula" not in request.QUERY_PARAMS:
            return Response({"formula": "Can not be empty"},
                            status=status.HTTP_400_BAD_REQUEST)
        if "variables" not in request.QUERY_PARAMS:
            return Response({"variables": "Can not be empty"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            variables = validate_variables(
                json.loads(request.QUERY_PARAMS["variables"]))
            validate_formula(request.QUERY_PARAMS["formula"], variables)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response(
                {"variables": "Unable to parse json: {}".format(e)},
                status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(e.error_dict, status=status.HTTP_400_BAD_REQUEST)


class NormalizersList(APIView):
    def get(self, request):
        normalizers = get_normalizers().values()
        serializer = NormalizerSerializer(normalizers, many=True)
        return Response(serializer.data)


class MetricsCreate(generics.ListCreateAPIView):
    model = Metric
    serializer_class = MetricSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'
    permission_classes = IsAuthenticatedOrReadOnly,

    def pre_save(self, obj):
        obj.creator_path = self.request.user.resource_path


class MetricsDetail(generics.RetrieveAPIView):
    model = Metric
    serializer_class = MetricSerializer


class MetriscOperationalize(APIView):
    permission_classes = IsAuthenticatedOrReadOnly,

    def post(self, request, metrics_id: int):
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
          ],
          "unit_id": 0
        }
        """

        # check if metric exists
        metric = Metric.objects.get(pk=metrics_id)
        if Metric.objects.get(pk=metrics_id) is None:
            return Response("Unable to find metric %s." % pk,
                            status=status.HTTP_404_NOT_FOUND)

        # check resquest data
        serializer = OperationalizeSerializer(data=request.DATA,
                                              files=request.FILES)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        # check if dateset with that title and acronym already existed
        title = serializer.object.get("title")
        acronym = serializer.object.get("acronym")
        error = {}
        if len(datasets.filter(title=title)) != 0:
            error["title"] = "Dataset name is not unique."
        if len(datasets.filter(acronym=acronym)) != 0:
            error["acronym"] = "Dataset acronym is not unique."
        if len(error) != 0:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        result_unit = serializer.object.get("unit_id")

        # load required data sets
        id_mapping = serializer.object.get("datasets")
        mapping = {variable: datasets.get(dataset_id) for
                   (variable, dataset_id) in id_mapping.items()}

        # ensure all datasets have the same class
        first_dataset = next(iter(mapping.values()))
        if not all([dataset.class_id == first_dataset.class_id
                    for dataset in mapping.values()]):
            return Response(
                {"datasets": "All datasets need to have the same class"})
        result_class = first_dataset.class_id

        # ensure all datasets have the same time_resolution
        if not all([dataset.data.resolution == first_dataset.data.resolution
                    for dataset in mapping.values()]):
            return Response({"datasets": "All datasets need to have the same time resolution"})
        result_time_resolution = first_dataset.data.resolution

        # compute result
        result = compute_formula(metric.formula, mapping)

        # collect remaining time slots
        result = result.dropna('index', 'all')
        # result_time_slots = result.index.values

        # dataset
        data = DatasetData(
            data_frame=result,
            unit=result_unit,
            resolution=result_time_resolution)

        result_time_start = data.get_time_start()
        result_time_end = data.get_time_end()

        dataset = Dataset(
            title=title,
            acronym=acronym,
            description="Computed formula '%s' with %s" % (
                metric.formula,
                ", ".join(["'%s' as %s" % (dataset.title, variable) for
                           variable, dataset in mapping.items()])),
            keywords=", ".join(set(itertools.chain(
                [dataset.keywords for dataset in mapping.values()]))),
            version=0,
            # ressource related info
            resource_url=reverse("metrics-detail", kwargs={'pk': metrics_id}),
            resource_issued=datetime.now(),
            # metrics identifier
            is_applied=True,
            metric_id=metrics_id,
            # contained data
            time_resolution=result_time_resolution,
            time_start=result_time_start,
            time_end=result_time_end,
            data=data,
            # references to other services
            # TODO add useful values here
            language_id=0,
            creator_path=self.request.user.resource_path,
            unit_id=result_unit,
            indicator_id=metric.indicator_id,
            class_id=result_class)

        dataset_id = datasets.store(dataset)

        return Response({
            "dataset": {
                "id": dataset_id
            }
        })
