__author__ = 'fki'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework import generics
from .models import *
from .serializers import *
from .file_encoder import FileEncoder


class Base(APIView):

    def get(self, request):
        """
        :type request: Request
        :param request:
        :return:
        """
        result = {
            "Datasets": reverse('dataset-list', request=request),
            "Converter": reverse('converter', request=request),
        }
        return Response(result)



class DatasetList(generics.ListCreateAPIView):
    model = Dataset
    serializer_class = BaseDatasetSerializer
    paginate_by = 10
    paginate_by_param = 'page_size'
    permission_classes = IsAuthenticatedOrReadOnly,

    def post(self, request, *args, **kwargs):
        self.serializer_class = DetailDatasetSerializer

        return super(DatasetList, self).post(request, args, kwargs)

    def get_queryset(self):
        queryset = Dataset.objects.all()
        indicator_id = self.request.GET.get('indicator_id', '')

        if indicator_id:
            queryset = queryset.filter(indicator_id=indicator_id)

        return queryset


class DatasetDetail(generics.RetrieveUpdateDestroyAPIView):

    model = Dataset
    serializer_class = DetailDatasetSerializer


class Converter(APIView):
    """
    Serves the converter resource.
    """

    def post(self, request, *args, **kwargs):
        """
        Processes a POST request
        """
        files = request.FILES

        if 'file' in files:
            # File has to be named file
            file = files['file']
            encoder = FileEncoder(file)

            # Check if the file extension is supported
            if not encoder.is_supported():
                return Response({'error': 'File Extension is not supported'}, status=status.HTTP_400_BAD_REQUEST)

            # Encode the file
            try:
                encoding = encoder.encode()
            except:
                return Response({'error': "Invalid File"}, status=status.HTTP_400_BAD_REQUEST)

            # Build the result
            result = {
                'filename': file.name,
                'filesize': file.size,
                'result': encoding
            }
            return Response(result)

        return Response({'error': "No Form field 'file'"}, status=status.HTTP_400_BAD_REQUEST)