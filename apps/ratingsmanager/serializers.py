from rest_framework.serializers import Serializer, ModelSerializer, IntegerField
from .models import *


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating


class RatingVoteSerializer(ModelSerializer):
    class Meta:
        model = RatingVote


class VoteSerializer(Serializer):
    score = IntegerField(min_value=1, max_value=5)
