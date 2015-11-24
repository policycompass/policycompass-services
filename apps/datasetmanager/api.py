import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http.response import HttpResponse
from policycompass_services import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .file_encoder import FileEncoder
from .serializers import *

__author__ = 'fki'


class Base(APIView):
    def get(self, request):
        """
        :type request
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

    def pre_save(self, obj):
        obj.creator_path = self.request.user.resource_path

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
    permission_classes = permissions.IsCreatorOrReadOnly,


class Converter(APIView):
    """
    Serves the converter resource.
    """

    def process_file(file):
        # File has to be named file
        encoder = FileEncoder(file)

        # Check if the file extension is supported
        if not encoder.is_supported():
            return Response({'error': 'File Extension is not supported'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Encode the file
        try:
            encoding = encoder.encode()
        except:
            return Response({'error': "Invalid File"},
                            status=status.HTTP_400_BAD_REQUEST)
        # Build the result
        result = {
            'filename': file.name,
            'filesize': file.size,
            'result': encoding
        }
        return Response(result)

    def post(self, request, *args, **kwargs):
        """
        Processes a POST request
        """
        files = request.FILES

        if 'file' in files:
            return Converter.process_file(files['file'])

        return Response({'error': "No Form field 'file'"},
                        status=status.HTTP_400_BAD_REQUEST)


class CKANSearchProxy(APIView):
    # FIXME Potential DDoS Source. Remove once EDP Auth is gone.
    def get(self, request, *args, **kwargs):
        apiBase = request.GET.get('api')
        term = request.GET.get('q')
        start = request.GET.get('start')
        if start is None:
            start = "0"

        if apiBase is None or term is None:
            return Response({'error': 'Invalid parameters.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # FIXME remove Auth
        r = requests.get(
            "%s/action/package_search?start=%s&q=%s&fq=%%28res_format:CSV%%20OR%%20res_format:TSV%%20OR%%20res_format:XLS%%20OR%%20res_format:XLSX%%29" %
            (apiBase, start, term),
            auth=('odportal', 'odp0rt4l$12'))

        if r.status_code == 200:
            return Response(r.json(), status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Server error. Check the logs.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CKANDownloadProxy(APIView):
    def get(self, request, *args, **kwargs):
        apiBase = request.GET.get('api')
        resourceId = request.GET.get('id')
        doConvert = request.GET.get('convert')

        if apiBase is None or resourceId is None:
            return Response({'error': 'Invalid parameters.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # FIXME remove Auth
        r = requests.get(
            "%s/action/resource_show?id=%s" % (apiBase, resourceId),
            auth=('odportal', 'odp0rt4l$12'))

        if r.status_code is not 200:
            return Response({'error': 'Server error. Check the logs.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        json = r.json()

        data = requests.get(json['result']['url'])

        if data.status_code is not 200:
            return Response({'error': 'Server error. Check the logs.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if doConvert is None:
            return HttpResponse(data.content,
                                content_type='application/octet-stream',
                                status=status.HTTP_200_OK)

        file = SimpleUploadedFile(
            name='file.%s' % (json['result']['format'].lower()),
            content=data.content,
            content_type='application/octet+stream')

        return Converter.process_file(file)
