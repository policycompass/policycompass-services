from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import index_utils

@api_view(['POST'])
def rebuildindex_service(request):
    """
    Rebuilds the elastic search index.
    """
    if request.method == 'POST':
        res = index_utils.rebuild_index()
        return Response(res)
