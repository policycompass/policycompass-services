from rest_framework import serializers
from .models import Extractor
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    policy_domains = serializers.SlugRelatedField(many=True, slug_field='domain', source='domains')
    creator_path = serializers.Field(source='creator_path')
    spatials = serializers.SlugRelatedField(many=True, slug_field='spatial', source='event_spatials')

    class Meta:
        model = Event


class CreateEventSerializer(EventSerializer):
    policy_domains = serializers.WritableField(source='policy_domains', required=True)
    spatials = serializers.WritableField(source='spatials')

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
    spatials = serializers.SlugRelatedField(many=True, slug_field='spatial', source='event_spatials')

    class Meta:
        model = Event
