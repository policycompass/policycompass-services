from rest_framework.serializers import ModelSerializer
from .models import *


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback


class FeedbackCategorySerializer(ModelSerializer):
    class Meta:
        model = FeedbackCategory
