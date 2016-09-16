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


@api_view(['POST'])
def rebuildindex_metric_service(request):
    """
    Rebuilds the elastic search index only for metrics.
    """
    if request.method == 'POST':
        res = index_utils.rebuild_index_itemtype('metric')
        return Response(res)


@api_view(['POST'])
def rebuildindex_visualization_service(request):
    """
    Rebuilds the elastic search index only for visualizations.
    """
    if request.method == 'POST':
        res = index_utils.rebuild_index_itemtype('visualization')
        return Response(res)


@api_view(['POST'])
def rebuildindex_event_service(request):
    """
    Rebuilds the elastic search index only for events.
    """
    if request.method == 'POST':
        res = index_utils.rebuild_index_itemtype('event')
        return Response(res)


@api_view(['POST'])
def rebuildindex_dataset_service(request):
    """
    Rebuilds the elastic search index only for datasets.
    """
    if request.method == 'POST':
        res = index_utils.rebuild_index_itemtype('dataset')
        return Response(res)


@api_view(['POST'])
def rebuildindex_indicator_service(request):
    """
    Rebuilds the elastic search index only for indicators.
    """
    if request.method == 'POST':
        res = index_utils.rebuild_index_itemtype('indicator')
        return Response(res)


@api_view(['POST'])
def rebuildindex_fuzzymap_service(request):
    """
    Rebuilds the elastic search index only for fuzzy maps.
    """
    if request.method == 'POST':
        res = index_utils.rebuild_index_fcm('fuzzymap')
        return Response(res)


@api_view(['POST'])
def rebuildindex_story_service(request):
    """
    Rebuilds the elastic search index only for stories.
    """
    if request.method == 'POST':
        res = index_utils.rebuild_index_itemtype('story')
        return Response(res)


@api_view(['POST'])
def rebuildindex_ag_service(request):
    """
    Rebuilds the elastic search index only for argumentation graphs.
    """
    if request.method == 'POST':
        res = index_utils.rebuild_index_itemtype('ag')
        return Response(res)


@api_view(['POST'])
def update_index_item_service(request, **kwargs):
    """
    Creates or updates a document index based on the id of the physical object.(Example to update 'metric' with id 26)
    """
    if request.method == 'POST':
        res = index_utils.update_index_item(kwargs.get('itemtype'),
                                            kwargs.get('itemid'))
        return Response(res)


@api_view(['POST'])
def delete_index_item_service(request, **kwargs):
    """
    Deletes a document index based on the id.(Example to delete index of type 'metric' with id 26)
    """
    if request.method == 'POST':
        res = index_utils.delete_index_item(kwargs.get('itemtype'),
                                            kwargs.get('itemid'))
        return Response(res)
