from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

class Base(APIView):

     def get(self, request, format=None):
        result = {
            "Rebuild Index Service": reverse('rebuildindex', request=request),
        }

        return Response(result)
