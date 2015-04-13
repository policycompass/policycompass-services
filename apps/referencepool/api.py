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


class DataClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DataClass.objects.all()
    serializer_class = DataClassSerializer


class IndividualViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IndividualSerializer

    def get_queryset(self):

        queryset = Individual.objects.all()
        data_class = self.request.QUERY_PARAMS.get('class', None)
        if data_class is not None:
            queryset = queryset.filter(data_class__id=data_class)
        return queryset


class ReferencePool(APIView):

    def get(self, request, format=None):
        result = {
            "Units": reverse('unit-list', request=request),
            "Unit Categories": reverse('unitcategory-list', request=request),
            "Languages": reverse('language-list', request=request),
            "Policy Domains": reverse('policydomain-list', request=request),
            "External Resources": reverse('externalresource-list', request=request),
            "Date Formats": reverse('dateformat-list', request=request),
            "Classes": reverse('class-list', request=request),
            "Individuals": reverse('individual-list', request=request)
        }
        return Response(result)