"""
Common Serializers.
"""


from rest_framework import serializers
from .models import User
from django.core.exceptions import ObjectDoesNotExist
import logging as log

class AuthSerializer(serializers.Serializer):
    """
    Serializer for User Sign in.
    DEPRECATED
    """
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=50)
    user = None

    def validate_email(self, attrs, source):
        try:
            self.user = User.objects.get(email=attrs[source])
            return attrs
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Email does not exist")

    def validate_password(self, attrs, source):
        if not self.user:
            return attrs
        else:
            if self.user.password != attrs[source]:
                raise serializers.ValidationError("Password is wrong")
            else:
                return attrs