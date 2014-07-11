from .models import HistoricalEvent
from rest_framework import viewsets
from .serializers import HistoricalEventSerializer


class HistoricalEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = HistoricalEvent.objects.all()
    serializer_class = HistoricalEventSerializer