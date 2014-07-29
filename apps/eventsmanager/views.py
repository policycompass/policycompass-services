from .models import Event
from .serializers import EventSerializer
from rest_framework import generics


class EventView(generics.ListCreateAPIView):
    model = Event
    serializer_class = EventSerializer


class EventInstanceView(generics.RetrieveUpdateDestroyAPIView):
    model = Event
    serializer_class = EventSerializer
