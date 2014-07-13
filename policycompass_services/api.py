__author__ = 'fki'

from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.urlresolvers import reverse


class Base(APIView):


     def get(self, request, format=None):
        result = {
            "Metrics Manager": request.build_absolute_uri(reverse('metric-list')),
            "Reference Pool": request.build_absolute_uri(reverse('reference-base')),
        }

        return Response(result)

