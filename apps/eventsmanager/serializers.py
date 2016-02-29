from rest_framework import serializers
from .models import Extractor
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    policy_domains = serializers.SlugRelatedField(many=True, slug_field='domain', source='domains')
    creator_path = serializers.Field(source='creator_path')

    class Meta:
        model = Event


class CreateEventSerializer(EventSerializer):
    policy_domains = serializers.WritableField(source='policy_domains', required=True)

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
    policy_domains = serializers.SlugRelatedField(many=True, slug_field='domain', source='domains')

    class Meta:
        model = Event
