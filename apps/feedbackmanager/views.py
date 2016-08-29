from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Feedback
from .serializers import *


class FeedbackListView(generics.ListCreateAPIView):
    # permission_classes = IsAuthenticatedOrReadOnly,
    queryset = Feedback.objects.all()
    # paginate_by = 10
    paginate_by_param = 'page_size'
    serializer_class = FeedbackSerializer


class FeedbackCategoryListView(generics.ListCreateAPIView):
    queryset = FeedbackCategory.objects.all()
    serializer_class = FeedbackCategorySerializer


class Base(APIView):
    def get(self, request):
        result = {
            "Feedbacks": reverse('feedback-list', request=request),
            "Feedback Categories": reverse('feedbackcategory-list', request=request)
        }
        return Response(result)
