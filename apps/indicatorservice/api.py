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

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateIndicatorSerializer
        return super(IndicatorViewSet, self).create(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = CreateIndicatorSerializer
        return super(IndicatorViewSet, self).update(request, args, kwargs)

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
