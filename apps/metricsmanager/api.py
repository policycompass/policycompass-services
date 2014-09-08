"""
Provides all views respectively API endpoints of the Metrics Manager.
"""

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, filters, generics
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction

import django_filters

from .serializers import *
from .models import Metric
from .schemas import *
from .file_encoder import FileEncoder

import logging
log = logging.getLogger(__name__)


class Base(APIView):
    """
    Serves the base resource.
    """
    def get(self, request):
        """
        Builds the representation for the GET method.
        """
        result = {
            "Metrics": reverse('metric-list', request=request),
            "Extra Categories": reverse('extra-list', request=request),
            "Converter": reverse('converter', request=request),
        }
        return set_jsonschema_link_header(Response(result), 'metrics_manager', request)


class MetricFilter(django_filters.FilterSet):
    """
    Configures the filter of the metric list.
    Based on Django Filters
    """
    external_resource = django_filters.Filter(name='ext_resource_id')
    language = django_filters.Filter(name='language_id')
    unit = django_filters.Filter(name='unit_id')
    policy_domain = django_filters.Filter(name='domains__domain_id')

    class Meta:
        """
        Sets the available filter
        """
        model = Metric
        fields = ['language', 'unit', 'external_resource', 'policy_domain']


class MetricList(APIView):
    """
    Serves the metric list resource.
    """
    #permission_classes = (IsAuthenticatedCanCreate,)
    parser_classes = (JSONParser,)
    # Sets the fields, which can be searched
    search_fields = ('title','keywords', 'acronym', 'geo_location')
    # Sets the fields, which are available for sorting the metrics
    ordering_fields = ('created_at', 'updated_at', 'title')

    def get(self, request):
        """
        Builds the representation for the GET method.
        """
        # Get all metrics
        queryset = Metric.objects.all()
        # Perform a search
        queryset = filters.SearchFilter().filter_queryset(self.request, queryset, self)
        # Order the set accordingly to query parameters
        queryset = filters.OrderingFilter().filter_queryset(self.request, queryset, self)
        # Filter the set by potential filters
        queryset = MetricFilter(request.GET, queryset=queryset)

        # Set the pagination
        paginator = Paginator(queryset, 10)
        page = request.QUERY_PARAMS.get('page')
        try:
            metrics = paginator.page(page)
        except PageNotAnInteger:
            metrics = paginator.page(1)
        except EmptyPage:
            metrics = paginator.page(paginator.num_pages)

        # Serialize the data
        serializer = PaginatedListMetricSerializer(metrics)

        return set_jsonschema_link_header(Response(serializer.data), 'metric_collection', request)

    @transaction.atomic  # Due to multiple DB accesses this method is atomic
    def post(self, request, *args, **kwargs):
        """
        Processes a POST request
        """
        # Serialize the provided data
        serializer = WriteMetricSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            # Take another Serializer, so IDs from the Reference Pool become full representations
            s = ReadMetricSerializer(serializer.object, context={'request': request})
            response = Response(s.data, status=status.HTTP_201_CREATED)
            # Add the Location Header
            response['Location'] = s.data['self']
            return set_jsonschema_link_header(response, 'metric', request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MetricDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Serves the metric resource
    """
    model = Metric
    serializer_class = ReadMetricSerializer

    def get(self, request, *args, **kwargs):
        """
        Builds the representation for the GET method.
        """
        response = super(MetricDetail, self).get(request, *args, **kwargs)
        return set_jsonschema_link_header(response, 'metric', request)

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        """
        Processes a PUT request
        """
        # Take the according serializer
        self.serializer_class = WriteMetricSerializer
        return super(MetricDetail, self).put(request, *args, **kwargs)


class ExtraCategoryList(generics.ListAPIView):
    """
    Serves the extra categories list resource.
    """

    model = RawDataCategory
    serializer_class = ExtraCategorySerializer

    def get(self, request, *args, **kwargs):
        """
        Builds the representation for the GET method.
        """
        response = super(ExtraCategoryList, self).get(request, *args, **kwargs)
        return set_jsonschema_link_header(response, 'category_collection', request)


class ExtraCategoryDetail(generics.RetrieveAPIView):
    """
    Serves the extra category resource.
    """

    model = RawDataCategory
    serializer_class = ExtraCategorySerializer

    def get(self, request, *args, **kwargs):
        """
        Builds the representation for the GET method.
        """
        response = super(ExtraCategoryDetail, self).get(request, *args, **kwargs)
        return set_jsonschema_link_header(response, 'category', request)


class Converter(APIView):
    """
    Serves the converter resource.
    """

    def get(self, request, format=None):
        """
        Builds the representation for the GET method.
        """
        return set_jsonschema_link_header(Response(), 'converter', request)

    def post(self, request, *args, **kwargs):
        """
        Processes a POST request
        """
        files = request.FILES

        if 'file' in files:
            # File has to be named file
            file = files['file']
            encoder = FileEncoder(file)

            # Check if the file extension is supported
            if not encoder.is_supported():
                return Response({'error': 'File Extension is not supported'}, status=status.HTTP_400_BAD_REQUEST)

            # Encode the file
            try:
                encoding = encoder.encode()
            except:
                return Response({'error': "Invalid File"}, status=status.HTTP_400_BAD_REQUEST)

            # Build the result
            result = {
                'filename': file.name,
                'filesize': file.size,
                'result': encoding
            }
            return set_jsonschema_link_header(Response(result), 'converter_result', request)

        return Response({'error': "No Form field 'file'"}, status=status.HTTP_400_BAD_REQUEST)


class SchemasView(APIView):
    """
    Serves JSON Hyper-Schema. The schema has to be in the schemas package.
    """

    def get(self, request, *args, **kwargs):
        """
        Returns the schema, which matches the name in the schema package.
        Naming convention in the schema package: {name}_schema
        """
        # Get the name from the url
        id = kwargs['name']
        schemas = Schemas()
        try:
            result = schemas.get_schema(id, request)
            return Response(result)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


def set_jsonschema_link_header(response, view, request):
    """
    Sets the link to the JSON Hyper-Schema in the Link-Header
    """
    context_url = reverse('schema-detail', request=request, args=(view,))
    response['Link'] = '<' + context_url + '>; rel="describedBy"'
    return response