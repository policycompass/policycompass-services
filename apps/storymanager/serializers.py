from rest_framework import serializers
from .models import Story, Chapter, Content


class StorySerializer(serializers.ModelSerializer):
    creator_path = serializers.Field(source='creator_path')

    chapters = serializers.SlugRelatedField(many=True, slug_field='chapter', source='story_chapters')

    class Meta:
        model = Story


class UpdateStorySerializer(StorySerializer):
    chapters = serializers.WritableField(source='chapters')

    class Meta:
        model = Story


class ExternalStorySerializer(serializers.Serializer):
    title = serializers.CharField()

    chapters = serializers.SlugRelatedField(many=True, slug_field='chapter', source='story_chapters')

    class Meta:
        model = Story


class ChapterSerializer(serializers.ModelSerializer):
    creator_path = serializers.Field(source='creator_path')

    contents = serializers.SlugRelatedField(many=True, slug_field='content', source='chapter_contents')

    class Meta:
        model = Chapter


class UpdateChapterSerializer(ChapterSerializer):
    title = serializers.CharField()
    text = serializers.CharField()
    contents = serializers.WritableField(source='contents')

    class Meta:
        model = Chapter


class ExternalChapterSerializer(serializers.Serializer):
    title = serializers.CharField()
    text = serializers.CharField()
    number = serializers.IntegerField()

    contents = serializers.SlugRelatedField(many=True, slug_field='content', source='chapter_contents')

    class Meta:
        model = Chapter


class ContentSerializer(serializers.ModelSerializer):
    creator_path = serializers.Field(source='creator_path')

    class Meta:
        model = Content


class UpdateContentSerializer(ContentSerializer):
    type = serializers.IntegerField()
    index = serializers.IntegerField()

    class Meta:
        model = Content


class ExternalContentSerializer(serializers.Serializer):
    type = serializers.IntegerField()
    index = serializers.IntegerField()

    class Meta:
        model = Content
