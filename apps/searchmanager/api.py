from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse


class Base(APIView):
    def get(self, request, format=None):
        result = {
            "Rebuild Index Service for all items": reverse('rebuildindex',
                                                           request=request),
            "Rebuild Index Service only for metrics": reverse(
                'rebuildindex_metric', request=request),
            "Rebuild Index Service only for visualizations": reverse(
                'rebuildindex_visualization', request=request),
            "Rebuild Index Service only for events": reverse(
                'rebuildindex_event', request=request),
            "Rebuild Index Service only for datasets": reverse(
                'rebuildindex_dataset', request=request),
            "Rebuild Index Service only for indicators": reverse(
                'rebuildindex_indicator', request=request),
            "Rebuild Index Service only for fuzzy maps": reverse(
                'rebuildindex_fuzzymap', request=request),
            "Rebuild Index Service only for stories": reverse(
                'rebuildindex_story', request=request),
            "Rebuild Index Service only for argumentation graphs": reverse(
                'rebuildindex_ag', request=request),
            "Create or Update Index for an itemtype ('metric','visualization','event','dataset','fuzzymap', 'indicator', 'story', 'ag')": reverse(
                'update_index_item', request=request,
                kwargs={'itemtype': 'metric', 'itemid': 26}),
            "Delete Index for an itemtype ('metric','visualization','event','dataset','fuzzymap', 'indicator', 'story', 'ag')": reverse(
                'delete_index_item', request=request,
                kwargs={'itemtype': 'metric', 'itemid': 26})
        }

        return Response(result)
