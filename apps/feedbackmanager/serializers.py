from rest_framework.serializers import Serializer, ModelSerializer, IntegerField
from .models import *


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
