from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework import pagination
from .models import *

__author__ = 'aos'


class ArgumentationGraphSerializer(ModelSerializer):
    creator_path = serializers.Field(source='creator_path')

    class Meta:
        model = ArgumentationGraph


class PaginatedListArgumentationGraphSerializer(
        pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = ArgumentationGraphSerializer
