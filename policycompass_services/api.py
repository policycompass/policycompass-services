from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from policycompass_services.permissions import IsAdhocracyGod
from policycompass_services.auth import AdhocracyAuthentication


class Base(APIView):
    def get(self, request, format=None):
        result = {
            "Dataset Manager": reverse('dataset-manager-base',
                                       request=request),
            "Metrics Manager": reverse('metrics-manager-base',
                                       request=request),
            "Reference Pool": reverse('reference-base', request=request),
            "Visualizations Manager": reverse('visualizations-manager-base',
                                              request=request),
            "Events Manager": reverse('event-base', request=request),
            "Ratings Manager": reverse('ratingsmanager-base', request=request),
            "Search Services": reverse('searchmanager-base', request=request),
            "Indicator Services": reverse('indicator-base', request=request),
            "Feedback Manager": reverse('feedbackmanager-base', request=request),
            "Story Manager": reverse('storymanager-base', request=request),
        }

        return Response(result)


class ExampleAuthenticated(APIView):
    authentication_classes = (AdhocracyAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return Response("Success")


class ExampleAdmin(APIView):
    authentication_classes = (AdhocracyAuthentication,)
    permission_classes = (IsAdhocracyGod,)

    def get(self, request, format=None):
        return Response("Success")
