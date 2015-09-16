__author__ = 'fki'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from policycompass_services.auth import AdhocracyAuthentication

class Base(APIView):

     def get(self, request, format=None):
        result = {
            "Dataset Manager": reverse('dataset-manager-base', request=request),
            "Metrics Manager": reverse('metrics-manager-base', request=request),
            "Reference Pool": reverse('reference-base', request=request),
            "Visualizations Manager": reverse('visualizations-manager-base', request=request),
            "Events Manager": reverse('event-base', request=request),
            "Search Services": reverse('searchmanager-base', request=request),
            "Indicator Services": reverse('indicator-base', request=request),
        }

        return Response(result)

class ExampleAuthenticated(APIView):

     authentication_classes = (AdhocracyAuthentication,)
     permission_classes = (IsAuthenticated,)

     def get(self, request, format=None):
          return Response("Success")

class ExampleAdmin(APIView):

     authentication_classes = (AdhocracyAuthentication,)
     permission_classes = (IsAdminUser,)

     def get(self, request, format=None):
          return Response("Success")
