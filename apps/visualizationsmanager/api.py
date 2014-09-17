from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import filters
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.parsers import JSONParser,YAMLParser
from .models import Visualization
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthenticatedCanCreate
#from .utils import get_rawdata_for_visualization
from django.db import IntegrityError, transaction
from rest_framework.reverse import reverse

from apps.metricsmanager.models import Metric
from apps.eventsmanager.models import Event
from apps.visualizationsmanager.models import HistoricalEventsInVisualizations

import django_filters

import logging
log = logging.getLogger(__name__)


class Base(APIView):

    def get(self, request, format=None):
        result = {
            "Visualizations": reverse('visualization-list', request=request),
            "Metrics": reverse('metric-list-for-visualization', request=request),
            "Events": reverse('event-list-for-visualization', request=request),
        }

        return Response(result)

'''
class VisualizationList(APIView):
    #permission_classes = (IsAuthenticatedCanCreate,)
    model = Visualization

    def options(self, request, *args, **kwargs):
        return Response("Options")

    def get(self, request):
        visualizations = Visualization.objects.all()
        serializer = ListVisualizationSerializer(visualizations, many=True, context={'request': request})
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = WriteVisualizationSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            log.info(serializer.object)
            s = ReadVisualizationSerializer(serializer.object, context={'request': request})
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
class EventDetailForVisualization(generics.RetrieveAPIView):
    model = Event
    serializer_class = HistoricalEventSerializer

class EventListForVisualization(generics.ListAPIView):
    model = Event
    serializer_class = HistoricalEventSerializer
    
    
class MetricDetailForVisualization(generics.RetrieveAPIView):
    model = Metric
    serializer_class = MetricSerializer

class MetricListForVisualization(generics.ListAPIView):
    model = Metric
    serializer_class = MetricSerializer
    
class VisualizationFilter(django_filters.FilterSet):
    #external_resource = django_filters.Filter(name='ext_resource_id')
    language = django_filters.Filter(name='language_id')

    class Meta:
        model = Visualization
        fields = ['language']


class VisualizationList(APIView):
    #permission_classes = (IsAuthenticatedCanCreate,)
    parser_classes = (JSONParser,)
    search_fields = ('title','keywords')
    ordering_fields = ('created_at', 'updated_at', 'title')
    def get(self, request):
        #logging.warning('....... get VisualizationList 1')
        queryset = Visualization.objects.all()
        queryset = filters.SearchFilter().filter_queryset(self.request, queryset, self)
        queryset = filters.OrderingFilter().filter_queryset(self.request, queryset, self)
        queryset = VisualizationFilter(request.GET, queryset=queryset)

        paginator = Paginator(queryset, 10)
        page = request.QUERY_PARAMS.get('page')

        try:
            visualizations = paginator.page(page)
        except PageNotAnInteger:
            visualizations = paginator.page(1)
        except EmptyPage:
            visualizations = paginator.page(paginator.num_pages)

        serializer = PaginatedListMetricSerializer(visualizations)

        #log.info(paginator.page_range)        
        #return set_jsonschema_link_header(Response(serializer.data), 'visualization_collection', request)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, *args, **kwargs):                    
        serializer = WriteVisualizationSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            s = ReadVisualizationSerializer(serializer.object, context={'request': request})
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class VisualizationDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Visualization
    serializer_class = ReadVisualizationSerializer
    #serializer_class = ReadVisualizationSerializer
'''    
def set_jsonschema_link_header(response, view, request):
    context_url = reverse('schema-detail', request=request, args=(view,))
    response['Link'] = '<' + context_url + '>; rel="describedBy"'
    return response
'''