import json

from django.core.exceptions import ValidationError
from django import shortcuts
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, status

from policycompass_services import permissions

from .serializers import *
from .normalization import get_normalizers
from . import formula, services


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
            "Calculator": reverse('calculate-dataset', request=request)
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

        formula_str = request.QUERY_PARAMS["formula"]
        try:
            variables = json.loads(request.QUERY_PARAMS["variables"])
        except ValueError as e:
            return Response(
                {"variables": "Unable to parse json: {}".format(e)},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            variables = formula.validate_variables(variables)
            formula.validate_formula(formula_str, variables)
        except ValidationError as e:
            return Response(e.error_dict, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


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


class MetricsDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Metric
    serializer_class = MetricSerializer
    permission_classes = permissions.IsCreatorOrReadOnly,


class DatasetCalculateView(APIView):
    permission_classes = IsAuthenticatedOrReadOnly,

    def post(self, request):
        """
        Compute a new dataset from a given formula and mappings.

        Example data:

        {
          "title": "Some test",
          "formula": "0.5 * norm(__1__, 0, 100) + 0.5 * norm(__2__, 0, 200)",
          "datasets": [
            {
              "variable": "__1__",
              "dataset": 1,
            },
            {
              "variable": "__1__",
              "dataset": 1,
            }
          ],
          "indicator_id": 0,
          "unit_id": 0,
        }
        """

        # check resquest data
        serializer = CalculateSerializer(data=request.DATA,
                                         files=request.FILES)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        data = serializer.object

        try:
            formula.validate_formula(data["formula"], data["datasets"])
            data = services.validate_operationalize(data)
        except ValidationError as e:
            return Response(e.error_dict, status=status.HTTP_400_BAD_REQUEST)

        creator_path = self.request.user.resource_path
        dataset_id = services.compute_dataset(
            creator_path=creator_path,
            **data)

        return Response({
            "dataset": {
                "id": dataset_id
            }
        })


class MetriscOperationalize(APIView):
    permission_classes = IsAuthenticatedOrReadOnly,

    def post(self, request, metrics_id: int):
        """
        Compute a new dataset from a given metric and mappings for variables.

        Example data:

        {
          "title" : "Some test",
          "datasets": [
            {
              "variable": "__1__",
              "dataset": 1,
            }
          ],
          "unit_id": 0,
        }
        """

        # check if metric exists
        metric = shortcuts.get_object_or_404(Metric, pk=metrics_id)

        # check resquest data
        serializer = OperationalizeSerializer(data=request.DATA,
                                              files=request.FILES)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        data = serializer.object

        try:
            data = services.validate_operationalize(data)
        except ValidationError as e:
            return Response(e.error_dict, status=status.HTTP_400_BAD_REQUEST)

        creator_path = self.request.user.resource_path
        dataset_id = services.compute_dataset(
            creator_path=creator_path,
            formula=metric.formula,
            indicator_id=metric.indicator_id,
            metric_id=metric.pk,
            **data)

        return Response({
            "dataset": {
                "id": dataset_id
            }
        })
