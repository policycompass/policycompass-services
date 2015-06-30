__author__ = 'fki'

from .serializers import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse


class IndicatorViewSet(viewsets.ModelViewSet):
    pagination_serializer_class = PaginatedListIndicatorSerializer
    serializer_class = IndicatorSerializer
    queryset = Indicator.objects.all()
    paginate_by = 10
    paginate_by_param = 'page_size'


class Base(APIView):
    """
    Serves the base resource.
    """
    def get(self, request):
        """
        Builds the representation for the GET method.
        """
        result = {
            "Indicators": reverse('indicator-list', request=request),
            }
        return Response(result)
