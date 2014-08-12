from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import filters
from rest_framework import mixins
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.parsers import JSONParser

from .models import Metric
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthenticatedCanCreate
from .utils import get_rawdata_for_metric
from django.db import IntegrityError, transaction
from rest_framework.reverse import reverse
from .file_encoder import FileEncoder

import django_filters

import logging
log = logging.getLogger(__name__)


class Base(APIView):

    def get(self, request, format=None):
        result = {
            "Metrics": reverse('metric-list', request=request),
            "Extra Categories": reverse('extra-list', request=request),
        }

        return Response(result)


class MetricFilter(django_filters.FilterSet):
    external_resource = django_filters.Filter(name='ext_resource_id')
    language = django_filters.Filter(name='language_id')
    unit = django_filters.Filter(name='unit_id')
    policy_domain = django_filters.Filter(name='domains__domain_id')

    class Meta:
        model = Metric
        fields = ['language', 'unit', 'external_resource', 'policy_domain']


class MetricList(APIView):
    #permission_classes = (IsAuthenticatedCanCreate,)
    parser_classes = (JSONParser,)
    search_fields = ('title','keywords', 'acronym', 'geo_location')
    ordering_fields = ('created_at', 'updated_at', 'title')
    def get(self, request):

        queryset = Metric.objects.all()
        queryset = filters.SearchFilter().filter_queryset(self.request, queryset, self)
        queryset = filters.OrderingFilter().filter_queryset(self.request, queryset, self)
        queryset = MetricFilter(request.GET, queryset=queryset)

        paginator = Paginator(queryset, 10)
        page = request.QUERY_PARAMS.get('page')
        try:
            metrics = paginator.page(page)
        except PageNotAnInteger:
            metrics = paginator.page(1)
        except EmptyPage:
            metrics = paginator.page(paginator.num_pages)

        serializer = PaginatedListMetricSerializer(metrics)

        #log.info(paginator.page_range)

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

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        self.serializer_class = WriteMetricSerializer
        return super(MetricDetail, self).put(request, *args, **kwargs)


class ExtraCategoryList(generics.ListAPIView):
    model = RawDataCategory
    serializer_class = ExtraCategorySerializer


class ExtraCategoryDetail(generics.RetrieveAPIView):
    model = RawDataCategory
    serializer_class = ExtraCategorySerializer


class Converter(APIView):

    def get(self, request, format=None):
        return Response("Converter")

    def post(self, request, *args, **kwargs):
        log.info('Data: ' + str(request.DATA))
        log.info('File: ' + str(request.FILES))

        files = request.FILES

        if 'file' in files:
            file = files['file']
            encoder = FileEncoder(file)

            if not encoder.is_supported():
                return Response({'error': 'File Extension is not supported'}, status=status.HTTP_400_BAD_REQUEST)

            result = {
                'filename': file.name,
                'filesize': file.size,
                'result': encoder.encode()
            }
            return Response(result)

        return Response({'error': "No Form field 'file'"}, status=status.HTTP_400_BAD_REQUEST)
