import os
from django.core.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from .models import Event, Extractor
from .serializers import EventSerializer
from rest_framework import generics
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
import voluptuous as v
import datetime

from .extractor import getExtractors, loadExtractor

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

class HarvestEvents(APIView):

    def get(self, request, format=None):
        start = request.QUERY_PARAMS.get('start', None)
        if start is None:
            start = "0001-01-01"
        end = request.QUERY_PARAMS.get('end', None)
        if end is None:
            end = "2099-12-31"
        keyword = request.QUERY_PARAMS.get('keyword', None)
        if keyword is None:
            keyword = ""

        extractors = request.QUERY_PARAMS.get('extractors', None)
        extractors = extractors.split(",")
        selectedExtractors = []
        for extractor in extractors:
            selectedExtractors.append(extractor)

        output = []

        for name in selectedExtractors:
            for i in getExtractors():
                if name == i["name"]:
                    print("Loading extractor " + i["name"])
                    e = Extractor.objects.filter(name=i["name"])
                    if e and e[0].active:
                        extractor = loadExtractor(i)
                        extractor_return = extractor.run(start, end, keyword)

                        for dict in extractor_return:
                            self.validate_extractor_output(dict)
                        output.extend(extractor_return)
                    else:
                        print("Extractor " + i["name"] + " not activated!")


        #Example Request: http://localhost:8000/api/v1/eventsmanager/harvestevents?start=1968-10-30&end=1980-12-31&keyword=war
        return Response(output)

    def validate_extractor_output(self, output):

        schema = v.Schema({
            v.Required("description"): str,
            v.Required("title"): str,
            v.Required("url"): str,
            v.Required("date"): self.Timestamp,
        })

        try:
            schema(output)
        except v.Invalid as e:
            raise ValidationError(e)

    def Timestamp(self, value):
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")



class ConfigExtractor(APIView):

    def get(self, request, format=None):

        name = request.QUERY_PARAMS.get('name', None)
        active = request.QUERY_PARAMS.get('active', None)

        if name!=None and name!="" and active!=None and active!="":
            e = Extractor.objects.all().filter(name="Alan")[0]
            if active == "true":
                e.active = True
            elif active == "false":
                e.active = False
            e.save()

        output = []
        e = Extractor.objects.all()
        for extractor in e:
            output.append({"name": extractor.name, "active": extractor.active})

        return Response(output)

class ConfigUpload(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        name = request.DATA['name']
        script_content = request.DATA['script']

        if name != None and name !="" and script_content != None and script_content !="":

            e = Extractor(name=name,active=True)
            e.save()

            if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/extractors/" + name):
                os.makedirs(os.path.dirname(os.path.abspath(__file__)) + "/extractors/" + name)
                with open(os.path.dirname(os.path.abspath(__file__)) + "/extractors/" + name + "/__init__.py", "w") as f:
                    f.write(script_content)

        return Response({'received data': request.DATA})

