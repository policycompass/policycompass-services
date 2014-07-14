__author__ = 'fki'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse


class Base(APIView):


     def get(self, request, format=None):
        result = {
            "Metrics Manager": reverse('metrics-manager-base', request=request),
            "Reference Pool": reverse('reference-base', request=request),
        }

        return Response(result)

