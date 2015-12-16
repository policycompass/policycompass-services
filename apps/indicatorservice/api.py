from .serializers import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from policycompass_services import permissions

__author__ = 'fki'


class IndicatorViewSet(viewsets.ModelViewSet):
    pagination_serializer_class = PaginatedListIndicatorSerializer
    serializer_class = IndicatorSerializer
    queryset = Indicator.objects.all()
    paginate_by = 10
    paginate_by_param = 'page_size'
    permission_classes = IsAuthenticatedOrReadOnly,

    def list(self, request, *args, **kwargs):
        params = request.QUERY_PARAMS
        if 'paginate' in params and params['paginate'] == 'false':
            self.paginate_by = None
        return super(IndicatorViewSet, self).list(request, args, kwargs)

    def pre_save(self, obj):
        obj.creator_path = self.request.user.resource_path

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateIndicatorSerializer
        return super(IndicatorViewSet, self).create(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = CreateIndicatorSerializer
        self.permission_classes = permissions.IsCreatorOrReadOnly,
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
