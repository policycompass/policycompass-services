from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.reverse import reverse
from rest_framework import viewsets

__author__ = 'fki'


class PolicyDomainViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PolicyDomain.objects.all()
    serializer_class = PolicyDomainSerializer


class UnitCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UnitCategory.objects.all()
    serializer_class = UnitCategorySerializer


class UnitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UnitSerializer

    def get_queryset(self):

        queryset = Unit.objects.all()
        category = self.request.QUERY_PARAMS.get('category', None)
        if category is not None:
            try:
                category = int(category)
                queryset = queryset.filter(unit_category__id=category)
            except ValueError:
                queryset = queryset.filter(unit_category__title=category)
        return queryset


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
        search_query = self.request.QUERY_PARAMS.get('q', None)
        search_query_backup = search_query
        if data_class is not None:
            try:
                data_class = int(data_class)
                queryset = queryset.filter(data_class__id=data_class)
            except ValueError:
                queryset = queryset.filter(data_class__title=data_class)
        if search_query is not None:
            try:
                found_individuals = False
                _queryset = []
                while found_individuals is False and len(search_query) > 3:
                    q = queryset
                    q = q.filter(title__icontains=search_query)
                    if len(q) > 0:
                        for i in range(0, len(q)):
                            if q[i] not in _queryset:
                                _queryset.append(q[i])
                                found_individuals = True
                    else:
                        search_query = search_query[:-1]

                search_query = search_query_backup
                found_individuals = False
                while found_individuals is False and len(search_query) > 3:
                    q = queryset
                    q = q.filter(title__icontains=search_query)
                    if len(q) > 0:
                        for i in range(0, len(q)):
                            if q[i] not in _queryset:
                                _queryset.append(q[i])
                            found_individuals = True
                    else:
                        search_query = search_query[1:]

                queryset = _queryset
            except:
                queryset = queryset

        return queryset


class LicenseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer


class ReferencePool(APIView):
    def get(self, request, format=None):
        result = {
            "Units": reverse('unit-list', request=request),
            "Unit Categories": reverse('unitcategory-list', request=request),
            "Languages": reverse('language-list', request=request),
            "Policy Domains": reverse('policydomain-list', request=request),
            "External Resources": reverse('externalresource-list',
                                          request=request),
            "Date Formats": reverse('dateformat-list', request=request),
            "Classes": reverse('class-list', request=request),
            "Individuals": reverse('individual-list', request=request),
            "Licenses": reverse('license-list', request=request)
        }
        return Response(result)
