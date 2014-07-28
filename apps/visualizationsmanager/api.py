from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Visualization
from .serializers import WriteVisualizationSerializer, ReadVisualizationSerializer, ListVisualizationSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthenticatedCanCreate
from .utils import get_rawdata_for_visualization
from django.db import IntegrityError, transaction
from rest_framework.reverse import reverse

import logging
log = logging.getLogger(__name__)


class Base(APIView):

    def get(self, request, format=None):
        result = {
            "Visualizations": reverse('visualization-list', request=request),
        }

        return Response(result)


class VisualizationList(APIView):
    #permission_classes = (IsAuthenticatedCanCreate,)
    model = Visualization

    def options(self, request, *args, **kwargs):
        return Response("Options")

    def get(self, request):
        visualization = Visualization.objects.all()
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


class VisualizationDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Visualization
    serializer_class = ReadVisualizationSerializer
