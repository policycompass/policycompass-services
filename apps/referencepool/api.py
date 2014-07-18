__author__ = 'fki'

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.reverse import reverse


class Base(APIView):

     def get(self, request, format=None):
        result = {
            "Units": reverse('unit-list', request=request),
            "Unit Categories": reverse('unit-category-list', request=request),
            "Languages": reverse('language-list', request=request),
            "Policy Domains": reverse('domain-list', request=request),
            "External Resources": reverse('resource-list', request=request),
        }

        return Response(result)


class UnitList(generics.ListAPIView):
    model = Unit
    serializer_class = UnitSerializer


class UnitDetail(generics.RetrieveAPIView):
    model = Unit
    serializer_class = UnitSerializer


class UnitCategoryList(generics.ListAPIView):
    model = UnitCategory
    serializer_class = UnitCategorySerializer


class UnitCategoryDetail(generics.RetrieveAPIView):
    model = UnitCategory
    serializer_class = UnitCategorySerializer


class LanguageList(generics.ListAPIView):
    model = Language
    serializer_class = LanguageSerializer


class LanguageDetail(generics.RetrieveAPIView):
    model = Language
    serializer_class = LanguageSerializer


class ExternalResourceList(generics.ListAPIView):
    model = ExternalResource
    serializer_class = ExternalResourceSerializer


class ExternalResourceDetail(generics.RetrieveAPIView):
    model = ExternalResource
    serializer_class = ExternalResourceSerializer


class PolicyDomainList(generics.ListAPIView):
    model = PolicyDomain
    serializer_class = PolicyDomainSerializer


class PolicyDomainDetail(generics.RetrieveAPIView):
    model = PolicyDomain
    serializer_class = PolicyDomainSerializer