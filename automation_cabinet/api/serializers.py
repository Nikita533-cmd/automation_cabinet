"""Сериализаторы для API."""
import base64
from collections import Counter

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers

from elements.models import (
    Automat, Contactor
)


class AutomatSerializer(serializers.ModelSerializer):
    """Сериализатор для связующей модели игредиент-рецепт с полем 'amount'."""

    class Meta:
        model = Automat
        fields = ('mass', 'price', 'name', 'i', 'Phase', 'A', 'B', 'C', 'Path', 'fiksator')

class Response2Serializer(serializers.Serializer):
    """Сериализатор для связующей модели игредиент-рецепт с полем 'amount'."""
    X = serializers.FloatField()
    Y = serializers.FloatField()
    Z = serializers.FloatField()
    path = serializers.CharField()
    
class ResponseSerializer(serializers.Serializer):
    """Сериализатор для связующей модели игредиент-рецепт с полем 'amount'."""
    count = serializers.IntegerField()
    elements = Response2Serializer(many=True)


class RequestSerializer(serializers.Serializer):
    """Сериализатор для связующей модели игредиент-рецепт с полем 'amount'."""
    power = serializers.FloatField()
    count = serializers.IntegerField()
    checkbox_AVR = serializers.BooleanField()
    outlet = serializers.IntegerField()
    def validate(self, attrs):
        return super().validate(attrs)
    # def to_representation(self, instance):
    #     return ResponseSerializer(instance, context=self.context).data
