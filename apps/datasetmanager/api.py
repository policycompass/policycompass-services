__author__ = 'fki'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics
from .models import *
from .serializers import *


class Base(APIView):

    def get(self, request):
        """
        :type request: Request
        :param request:
        :return:
        """
        result = {
            "Datasets": reverse('dataset-list', request=request),
        }
        return Response(result)



class DatasetList(generics.ListCreateAPIView):
    model = Dataset
    serializer_class = BaseDatasetSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'

    def post(self, request, *args, **kwargs):
        self.serializer_class = DetailDatasetSerializer

        return super(DatasetList, self).post(request, args, kwargs)

class DatasetDetail(generics.RetrieveUpdateDestroyAPIView):

    model = Dataset
    serializer_class = DetailDatasetSerializer