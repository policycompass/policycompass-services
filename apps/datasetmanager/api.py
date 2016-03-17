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
from collections import OrderedDict
import json

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
        self.serializer_class = UpdateDatasetSerializer

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

    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateDatasetSerializer
        return super(DatasetDetail, self).put(request, args, kwargs)


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


class EurostatSearchProxy(APIView):
    def get(self, request, *args, **kwargs):
        apiBase = request.GET.get('api')
        term = request.GET.get('q')
        start = request.GET.get('start')
        if start is None:
            start = "0"

        if apiBase is None or term is None:
            return Response({'error': 'Invalid parameters.'},
                            status=status.HTTP_400_BAD_REQUEST)

        request = "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/" + str(term) + "?precision=1"

        data = requests.get(request)

        if data.status_code == 400:
            return Response({'error': 'Could not find Database'}, status=status.HTTP_400_BAD_REQUEST)
        elif data.status_code == 416:
            return Response({'error': 'Too many categories have been requested. Maximum is 50'}, status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)

        array = data.json(object_pairs_hook=OrderedDict)

        dimensions = array['dimension']
        dimensionsList = list(dimensions)

        filtersList = dimensionsList

        filtersDetailList = {}

        filtersDetailList.update({'label': array['label']})

        for f in range(0, len(filtersList)):
            filter = array['dimension'][filtersList[f]]['category']['label']
            filterList = list(filter)
            filterKeys = list(filter.keys())
            filterValues = list(filter.values())

            newFilterList = []

            for i in range(0, len(filterList)):
                newFilter = [filterKeys[i], filterValues[i]]
                newFilterList.append(newFilter)

            filtersDetailList.update({filtersList[f]: newFilterList})

        filters = {"result": filtersDetailList}
        filtersString = str(filters).replace("'", '"')
        filterJson = json.loads(filtersString)

        if data.status_code == 200:
            return Response(filterJson, status=status.HTTP_200_OK)
        elif data.status_code == 400:
            return Response({'error': 'Could not find Database'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Server error. Check the logs.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EurostatDownloadProxy(APIView):
    def get(self, request, *args, **kwargs):
        dataset = request.GET.get('dataset')
        filtersString = request.GET.get('filters')
        filters = {}
        query = " "

        if filtersString is None:
            filtersString = {'result': ''}

        else:
            filters = json.loads(filtersString)

        filters = filters.get('result')
        if(filters):
            for key in range(0, len(filters)):
                for value in range(0, len(filters[key][1])):
                    query += '&' + filters[key][0] + '=' + filters[key][1][value]

        data = requests.get("http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/" + str(dataset) + "?precision=1" + query.strip())

        if data.status_code == 400:
            return Response({'error': 'Could not find Database'}, status=status.HTTP_400_BAD_REQUEST)
        elif data.status_code == 416:
            return Response({'error': 'Too many categories have been requested. Maximum is 50'}, status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)

        array = data.json(object_pairs_hook=OrderedDict)

        rowHeaders = array['dimension']['geo']['category']['label']

        rowHeadersValues = list(rowHeaders.values())

        rowLen = len(rowHeadersValues)

        colHeaders = array['dimension']['time']['category']['label']

        colHeadersVals = list(colHeaders.values())

        colLen = len(colHeadersVals) + 1

        colHeadersValues = []

        colHeadersValues.append("")

        for q in range(0, colLen - 1):
            colHeadersValues.append(colHeadersVals[q])

        val = array['value']

        values = list(val.values())

        rowArrays = []

        index = 0
        for row in range(0, rowLen):
            colArray = []
            position = row * (colLen - 1)
            colArray.append(rowHeadersValues[row])
            for col in range(0, colLen - 1):
                if val.get(str(position + col)) is None:
                    colArray.append("")
                else:
                    colArray.append(values[index])
                    index += 1

            rowArrays.append(colArray)

        resultArray = []
        resultArray.append(colHeadersValues)

        for y in range(0, len(rowArrays)):
            resultArray.append(rowArrays[y])

        result = {
            'filename': 'file.xls',
            'filesize': 500000,
            'result': resultArray
        }

        return Response(result)


class CKANSearchProxy(APIView):
    # FIXME Potential DDoS Source. Remove once EDP Auth is gone.
    def get(self, request, *args, **kwargs):
        apiBase = request.GET.get('api')
        print("APIBASE " + apiBase)
        print("q " + request.GET.get('q'))
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
