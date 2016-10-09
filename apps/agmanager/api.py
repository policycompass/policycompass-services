from .serializers import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from policycompass_services import permissions

__author__ = 'fki'


class ArgumentationGraphViewSet(viewsets.ModelViewSet):
    model = ArgumentationGraph
    pagination_serializer_class = PaginatedListArgumentationGraphSerializer
    serializer_class = ArgumentationGraphSerializer
    queryset = ArgumentationGraph.objects.all()
    paginate_by = 10
    paginate_by_param = 'page_size'
    permission_classes = IsAuthenticatedOrReadOnly,

    def list(self, request, *args, **kwargs):
        params = request.QUERY_PARAMS
        if 'paginate' in params and params['paginate'] == 'false':
            self.paginate_by = None
        return super(ArgumentationGraphViewSet, self).list(request, args,
                                                           kwargs)

    def pre_save(self, obj):
        obj.creator_path = self.request.user.resource_path

    def create(self, request, *args, **kwargs):
        self.serializer_class = ArgumentationGraphSerializer
        return super(ArgumentationGraphViewSet, self).create(request, args,
                                                             kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = ArgumentationGraphSerializer
        self.permission_classes = permissions.IsCreatorOrReadOnly,
        return super(ArgumentationGraphViewSet, self).update(request, args,
                                                             kwargs)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        user = request.user.resource_path
        ag = ArgumentationGraph.objects.get(id=id)

        if ag.creator_path == user or request.user.is_admin is True:
            ag.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': "User does not have the necessary permissions"}, status=status.HTTP_403_FORBIDDEN)


class Base(APIView):
    """
    Serves the base resource.
    """

    def get(self, request):
        """
        Builds the representation for the GET method.
        """
        result = {
            "Argumentation Graphs": reverse('ag-list',
                                            request=request),
        }
        return Response(result)
