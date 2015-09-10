import os
from .models import Event
from .serializers import EventSerializer
from rest_framework import generics
from datetime import datetime
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .extractor import getExtractors, loadExtractor

import json

class Base(APIView):

     def get(self, request, format=None):
        result = {
            "Events": reverse('author-list', request=request),
        }
        return Response(result)

class EventView(generics.ListCreateAPIView):
    model = Event
    serializer_class = EventSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    def get_queryset(self):
        def validate_date(d):
            try:
                datetime.strptime(d, '%Y-%m-%d')
                return True
            except ValueError:
                return False
        queryset = Event.objects.all()
        title = self.request.QUERY_PARAMS.get('title', None)
        start = self.request.QUERY_PARAMS.get('start', None)
        end = self.request.QUERY_PARAMS.get('end', None)
        time_resolution = self.request.QUERY_PARAMS.get('time_resolution', None)
        if start and end is not None:
            if time_resolution is not None:
                if time_resolution == 'year':
                    start = start + '-01-01'
                    end = end + '-12-31'
                elif time_resolution == 'month':
                    start = start + '-01'
                    end = end + '-31'
                elif time_resolution == 'quarter':
                    if start[-2:].lower() == 'q1':
                        start = start[:4] + '-01-01'
                    elif start[-2:].lower() == 'q2':
                        start = start[:4] + '-04-01'
                    elif start[-2:].lower() == 'q3':
                        start = start[:4] + '-07-01'
                    elif start[-2:].lower() == 'q4':
                        start = start[:4] + '-10-01'
                    if end[-2:].lower() == 'q1':
                        end = end[:4] + '-03-31'
                    elif end[-2:].lower() == 'q2':
                        end = end[:4] + '-06-30'
                    elif end[-2:].lower() == 'q3':
                        end = end[:4] + '-09-30'
                    elif end[-2:].lower() == 'q4':
                        end = end[:4] + '-12-31'
            if validate_date(start) and validate_date(end) is not None:
                queryset2 = queryset
                queryset = queryset.filter(Q(startEventDate__range=[start, end]) | Q(endEventDate__range=[start, end]))
                queryset = queryset | queryset2.filter(startEventDate__lte=start).filter(endEventDate__gte=end)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset


class EventInstanceView(generics.RetrieveUpdateDestroyAPIView):
    model = Event
    serializer_class = EventSerializer

@api_view(['GET'])
def harvest_events(request):

    start = request.QUERY_PARAMS.get('start', None)
    if start is None:
        start = "0001-01-01"
    end = request.QUERY_PARAMS.get('end', None)
    if end is None:
        end = "2099-12-31"
    keyword = request.QUERY_PARAMS.get('keyword', None)
    if keyword is None:
        keyword = ""
    output = []
    for i in getExtractors():
        print("Loading plugin " + i["name"])
        plugin = loadExtractor(i)
        output.extend(plugin.run(start, end, keyword))


    #Example Request: http://localhost:8000/api/v1/eventsmanager/harvestevents?start=1968-10-30&end=1980-12-31&keyword=war
    return Response(output)

@api_view(['GET'])
def config_extractor(request):

    name = ""
    name = request.QUERY_PARAMS.get('name', None)
    if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/extractors/" + name):
        os.makedirs(os.path.dirname(os.path.abspath(__file__)) + "/extractors/" + name)
        with open(os.path.dirname(os.path.abspath(__file__)) + "/extractors/" + name + "/__init__.py", "w") as f:
            f.write("FOOBAR")

    return Response(name)