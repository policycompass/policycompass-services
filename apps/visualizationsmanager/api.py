from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, filters
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.parsers import JSONParser
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db import transaction
from rest_framework.reverse import reverse
from rest_framework.generics import strict_positive_int
from policycompass_services import permissions
import django_filters
import logging

log = logging.getLogger(__name__)


class Base(APIView):
    def get(self, request, format=None):
        result = {
            "Visualizations": reverse('visualization-list', request=request),
            "Datasets": reverse('dataset-list-for-visualization',
                                request=request),
            "Events": reverse('event-list-for-visualization', request=request),
            "Visualizations linked by dataset": reverse(
                'linked-visualizations-by-dataset', request=request),
            "Visualizations linked by event": reverse(
                'linked-visualizations-by-event', request=request),
        }

        return Response(result)


class EventDetailForVisualization(generics.RetrieveAPIView):
    model = HistoricalEventsInVisualizations
    serializer_class = HistoricalEventSerializer


class EventListForVisualization(generics.ListAPIView):
    model = HistoricalEventsInVisualizations
    serializer_class = HistoricalEventSerializer


class DatasetDetailForVisualization(generics.RetrieveAPIView):
    model = DatasetsInVisualizations
    serializer_class = DatasetSerializer


class DatasetListForVisualization(generics.ListAPIView):
    model = DatasetsInVisualizations
    serializer_class = DatasetSerializer


class VisualizationsLinkedByDataset(APIView):
    """
    Serves the visualizations linked by a dataset. ?dataset_id=#
    """
    # API to get visualizations related with a dataset by dataset id
    # permission_classes = (IsAuthenticatedCanCreate,)
    parser_classes = (JSONParser,)
    # Sets the fields, which can be searched
    search_fields = ('dataset_id')
    # Sets the fields, which are available for sorting
    ordering_fields = ('id')

    def get(self, request):
        """
        Builds the representation for the GET method.
        """
        # Get all Datasets In Visualizations
        # queryset = MetricsInVisualizations.objects.all()
        queryset = DatasetsInVisualizations.objects.all()

        # Perform a search
        queryset = filters.SearchFilter().filter_queryset(self.request,
                                                          queryset, self)
        # Order the set accordingly to query parameters
        queryset = filters.OrderingFilter().filter_queryset(self.request,
                                                            queryset, self)
        # Filter the set by potential filters
        queryset = VisualizationsLinkedByDatasetFilter(request.GET,
                                                       queryset=queryset)

        # Set the pagination
        page_size = 10
        request_page_size = request.QUERY_PARAMS.get('page_size')

        if request_page_size:
            try:
                page_size = strict_positive_int(request_page_size)
            except (KeyError, ValueError):
                pass

        # Set the pagination
        paginator = Paginator(queryset, page_size)
        page = request.QUERY_PARAMS.get('page')

        try:
            datasetsinvisualizations = paginator.page(page)
        except PageNotAnInteger:
            datasetsinvisualizations = paginator.page(1)
        except EmptyPage:
            datasetsinvisualizations = paginator.page(paginator.num_pages)
        # Serialize the data
        serializer = PaginatedListVisualizationLinkedByDatasetSerializer(
            datasetsinvisualizations)

        return Response(serializer.data)


class VisualizationsLinkedByDatasetFilter(django_filters.FilterSet):
    # API filter to get visualizations related with a dataset by dataset id'
    metric = django_filters.Filter(name='dataset_id')

    class Meta:
        model = DatasetsInVisualizations
        fields = ['dataset_id']


class VisualizationsLinkedByEvent(APIView):
    """
    Serves the visualizations linked by an event. ?historical_event_id=#.
    """
    # API to get visualizations related with an event by event id
    # permission_classes = (IsAuthenticatedCanCreate,)
    parser_classes = (JSONParser,)
    # Sets the fields, which can be searched
    search_fields = ('historical_event_id')
    # Sets the fields, which are available for sorting
    ordering_fields = ('id')

    def get(self, request):
        """
        Builds the representation for the GET method.
        """
        # Get all HE InVisualizations
        queryset = HistoricalEventsInVisualizations.objects.all()

        # Perform a search
        queryset = filters.SearchFilter().filter_queryset(self.request,
                                                          queryset, self)
        # Order the set accordingly to query parameters
        queryset = filters.OrderingFilter().filter_queryset(self.request,
                                                            queryset, self)
        # Filter the set by potential filters
        queryset = VisualizationsLinkedByEventFilter(request.GET,
                                                     queryset=queryset)

        # Set the pagination
        # set defaul
        page_size = 10
        # get url param
        request_page_size = request.QUERY_PARAMS.get('page_size')

        if request_page_size:
            try:
                page_size = strict_positive_int(request_page_size)
            except (KeyError, ValueError):
                pass

        # Set the pagination
        paginator = Paginator(queryset, page_size)
        page = request.QUERY_PARAMS.get('page')

        try:
            eventsinvisualizations = paginator.page(page)
        except PageNotAnInteger:
            eventsinvisualizations = paginator.page(1)
        except EmptyPage:
            eventsinvisualizations = paginator.page(paginator.num_pages)

        # Serialize the data
        serializer = PaginatedListVisualizationLinkedByEventSerializer(
            eventsinvisualizations)

        # log.info(paginator.page_range)
        # return set_jsonschema_link_header(Response(serializer.data), 'visualization_collection', request)
        return Response(serializer.data)


class VisualizationsLinkedByEventFilter(django_filters.FilterSet):
    # API filter to get visualizations related with an event by event id
    event = django_filters.Filter(name='historical_event_id')

    class Meta:
        model = HistoricalEventsInVisualizations
        fields = ['historical_event_id']


class VisualizationFilter(django_filters.FilterSet):
    language = django_filters.Filter(name='language_id')

    class Meta:
        model = Visualization
        fields = ['language']


class VisualizationList(APIView):
    """
    Serves the visualization list resource.
    """
    permission_classes = IsAuthenticatedOrReadOnly,
    parser_classes = (JSONParser,)
    # Sets the fields, which can be searched
    search_fields = ('title', 'keywords')
    # Sets the fields, which are available for sorting
    # ordering_fields = ('created_at', 'updated_at', 'title')
    ordering_fields = ('date_created', 'date_modified', 'title')

    def get(self, request):
        """
        Builds the representation for the GET method.
        """
        # Get all visualizations
        queryset = Visualization.objects.all()
        # Perform a search
        queryset = filters.SearchFilter().filter_queryset(self.request,
                                                          queryset, self)
        # Order the set accordingly to query parameters
        queryset = filters.OrderingFilter().filter_queryset(self.request,
                                                            queryset, self)
        # Filter the set by potential filters
        queryset = VisualizationFilter(request.GET, queryset=queryset)

        # Set the pagination
        # set defaul
        page_size = 10
        # get url param
        request_page_size = request.QUERY_PARAMS.get('page_size')

        if request_page_size:
            try:
                page_size = strict_positive_int(request_page_size)
            except (KeyError, ValueError):
                pass

        # Set the pagination
        paginator = Paginator(queryset, page_size)
        page = request.QUERY_PARAMS.get('page')

        try:
            visualizations = paginator.page(page)
        except PageNotAnInteger:
            visualizations = paginator.page(1)
        except EmptyPage:
            visualizations = paginator.page(paginator.num_pages)

        # Serialize the data
        serializer = PaginatedListDatasetSerializer(visualizations)

        # log.info(paginator.page_range)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = WriteVisualizationSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.object.creator_path = self.request.user.resource_path
            serializer.save()
            s = ReadVisualizationSerializer(serializer.object,
                                            context={'request': request})
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisualizationDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Visualization
    serializer_class = ReadVisualizationSerializer
    permission_classes = permissions.IsCreatorOrReadOnly,

    def put(self, request, *args, **kwargs):
        self.serializer_class = WriteVisualizationSerializer
        return super(VisualizationDetail, self).put(request, args, kwargs)
