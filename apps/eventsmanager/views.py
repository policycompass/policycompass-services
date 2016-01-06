import os
from django.core.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from .models import Event, Extractor
from .serializers import EventSerializer, ExtractorSerializer
from rest_framework import generics
from rest_framework import status
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from policycompass_services.auth import AdhocracyAuthentication
import voluptuous as v
import datetime
from .extractor_manager import getExtractors, loadExtractor


class Base(APIView):
    def get(self, request, format=None):
        result = {
            "Events": reverse('author-list', request=request),
            "Events Harvester": reverse('harvest-events', request=request),
            "Harvester Configurator": reverse('config-extractor',
                                              request=request),
        }
        return Response(result)


class EventView(generics.ListCreateAPIView):
    """
    Creates new events and returns a list of available event with filter options
    """
    model = Event
    serializer_class = EventSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    permission_classes = IsAuthenticatedOrReadOnly,

    def pre_save(self, obj):
        obj.creator_path = self.request.user.resource_path

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
        time_resolution = self.request.QUERY_PARAMS.get('time_resolution',
                                                        None)

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
                queryset = queryset.filter(
                    Q(startEventDate__range=[start, end]) | Q(
                        endEventDate__range=[start, end]))
                queryset = queryset | queryset2.filter(
                    startEventDate__lte=start).filter(endEventDate__gte=end)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset


class EventInstanceView(generics.RetrieveUpdateDestroyAPIView):
    model = Event
    serializer_class = EventSerializer


class HarvestEvents(APIView):
    """
    Searches in available data sources for events
    """
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
        selectedExtractors = []
        extractors = request.QUERY_PARAMS.get('extractors', None)
        if extractors is not None:
            extractors = extractors.split(",")
            for extractor in extractors:
                selectedExtractors.append(extractor)

        output = []

        for name in selectedExtractors:
            for i in getExtractors():
                if name == i["name"]:
                    print("Loading extractor " + i["name"])
                    e = Extractor.objects.filter(name=i["name"])
                    if e and e[0].active and e[0].valid:
                        extractor = loadExtractor(i)
                        extractor_return = extractor.run(start, end, keyword)
                        for dict in extractor_return:
                            dict["source"] = i["name"]
                        output.extend(extractor_return)
                    else:
                        print("Extractor " + i["name"] + " not activated!")

        for idx, item in enumerate(output):
            item["id"] = idx

        return Response(output)


class GetExtractor(APIView):
    def get(self, request, format=None):
        """
        Returns a list of all extractors.
        """
        queryset = Extractor.objects.all()
        serializer = ExtractorSerializer(queryset, many=True)
        return Response(serializer.data)


class ConfigExtractor(APIView):
    """
    Creates new datasources and validates them. activaes and deactivates existing data sources
    """
    # Only authenticate admins for this APIView
    authentication_classes = (AdhocracyAuthentication,)
    # permission_classes = (IsAuthenticated,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # permission_classes = (IsAdhocracyGod,)

    def patch(self, request, format=None):
        """
        Switches extractors on and off by changing the state in the Extractor Model.
        """
        name = request.DATA['name']
        active = request.DATA['active']

        if name is not None and name != "" and active is not None and active != "":
            e = Extractor.objects.all().filter(name=name)
            if e:
                e = e[0]
                if active == "true":
                    e.active = True
                elif active == "false":
                    e.active = False
                e.save()

        queryset = Extractor.objects.all()
        serializer = ExtractorSerializer(queryset, many=True)
        return Response(serializer.data)

    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        """
        Creates, validates and registers a new extractor and saves the uploaded script.
        """
        name = request.DATA['name']
        script_content = request.DATA['script']
        e = Extractor.objects.filter(name=name)

        if name is not None and name != "" and script_content is not None and script_content != "" and not e:

            valid = True

            if not os.path.exists(os.path.dirname(
                    os.path.abspath(__file__)) + "/extractors/" + name):
                os.makedirs(os.path.dirname(
                    os.path.abspath(__file__)) + "/extractors/" + name)
                with open(os.path.dirname(os.path.abspath(__file__)) + "/extractors/" + name + "/__init__.py", "w") as f:
                    f.write(script_content)

            try:
                for i in getExtractors():
                    if name == i["name"]:
                        print("Loading extractor " + i["name"])

                        extractor = loadExtractor(i)
                        extractor_return = extractor.run("1927-05-03",
                                                         "2015-09-09", "war")

                        for dict in extractor_return:
                            self.validate_extractor_output(dict)
            except:
                valid = False

            e = Extractor(name=name, active=True, valid=valid)
            e.save()

            if valid:
                return Response(request.DATA, status=status.HTTP_201_CREATED)

        return Response({'error': "Validation failed!"},
                        status=status.HTTP_400_BAD_REQUEST)

    def validate_extractor_output(self, output):
        """
        Validation function for the extractor output.
        """
        schema = v.Schema({
            v.Required("title"): str,
            v.Required("date"): self.Timestamp,
            ("description"): str,
            ("url"): str,
            ("enddate"): self.Timestamp,
            ("keywords"): str,
            ("geolocation"): str,
            ("language"): str,

        })

        try:
            schema(output)
        except v.Invalid as e:
            raise ValidationError(e)

    def Timestamp(self, value):
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
