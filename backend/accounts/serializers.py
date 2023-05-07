from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .validators import polish_email_validator

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(validators=[polish_email_validator, UniqueValidator])

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
        ]


class BaseUserPublicSerializer(serializers.ModelSerializer):
    email = serializers.CharField(validators=[polish_email_validator, UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password"
        ]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)
