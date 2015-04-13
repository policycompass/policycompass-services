__author__ = 'fki'

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.reverse import reverse
from rest_framework import viewsets


class PolicyDomainViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PolicyDomain.objects.all()
    serializer_class = PolicyDomainSerializer


class UnitCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UnitCategory.objects.all()
    serializer_class = UnitCategorySerializer


class UnitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ExternalResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExternalResource.objects.all()
    serializer_class = ExternalResourceSerializer


class DateFormatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DateFormat.objects.all()
    serializer_class = DateFormatSerializer


class ReferencePool(APIView):

    def get(self, request, format=None):
        result = {
            "Units": reverse('unit-list', request=request),
            "Unit Categories": reverse('unitcategory-list', request=request),
            "Languages": reverse('language-list', request=request),
            "Policy Domains": reverse('policydomain-list', request=request),
            "External Resources": reverse('externalresource-list', request=request),
            "Date Formats": reverse('dateformat-list', request=request),
        }
        return Response(result)