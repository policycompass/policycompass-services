from .models import Event
from .serializers import EventSerializer
from rest_framework import generics
from datetime import datetime
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response

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
        if start and end is not None:
            if validate_date(start) and validate_date(end) is not None:
                queryset2 = queryset
                queryset = queryset.filter(Q(startEventDate__range=[start, end]) | Q(endEventDate__range=[start, end]))
                queryset = queryset | queryset2.filter(startEventDate__lte=start).filter(endEventDate__gte=end)
        if title is not None:
            queryset = queryset.filter(title=title)
        return queryset


class EventInstanceView(generics.RetrieveUpdateDestroyAPIView):
    model = Event
    serializer_class = EventSerializer