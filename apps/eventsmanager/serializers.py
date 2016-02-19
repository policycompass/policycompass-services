from rest_framework import serializers
from .models import Extractor
from .models import Event
from rest_framework.serializers import WritableField


class EventSerializer(serializers.ModelSerializer):
    policy_domains = WritableField(source='policy_domains', required=True)
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
    policy_domains = WritableField(source='policy_domains', required=True)

    class Meta:
        model = Event
