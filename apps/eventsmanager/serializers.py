from rest_framework import serializers
from .models import Extractor
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    creator_path = serializers.Field(source='creator_path')

    class Meta:
        model = Event


class ExtractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extractor


class ExternalEventSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    url = serializers.CharField()
    start = serializers.DateTimeField()
    finish = serializers.DateTimeField()
