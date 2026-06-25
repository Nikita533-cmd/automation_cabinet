"""Сериализаторы для API."""
import base64
from collections import Counter

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers

from elements.models import (
    Automat, Contactor, Cabinet
)


class AutomatSerializer(serializers.ModelSerializer):
    """Сериализатор для связующей модели игредиент-рецепт с полем 'amount'."""

    class Meta:
        model = Automat
        fields = ('mass', 'price', 'name', 'i', 'Phase', 'A', 'B', 'C', 'Path', 'fiksator')


class CabinetSerializer(serializers.ModelSerializer):
    """Сериализатор для связующей модели игредиент-рецепт с полем 'amount'."""

    class Meta:
        model = Cabinet
        fields = ('mass', 'price', 'name', 'A', 'B', 'C', 'Path')



class Response2Serializer(serializers.Serializer):
    """Сериализатор для связующей модели игредиент-рецепт с полем 'amount'."""
    X = serializers.FloatField()
    Y = serializers.FloatField()
    Z = serializers.FloatField()
    path = serializers.CharField()
    
class ResponseSerializer(serializers.Serializer):
    """Сериализатор для связующей модели игредиент-рецепт с полем 'amount'."""
    mass = serializers.FloatField()
    price = serializers.FloatField()
    elements = Response2Serializer(many=True)
    cabinet = CabinetSerializer(read_only=True)

class OutsSerializer(serializers.Serializer):
    """Сериализатор для связующей модели игредиент-рецепт с полем 'amount'."""
    name = serializers.CharField()
    i = serializers.FloatField()


class RequestSerializer(serializers.Serializer):
    """Сериализатор для связующей модели игредиент-рецепт с полем 'amount'."""
    power = serializers.FloatField()
    count = serializers.IntegerField()
    checkbox_AVR = serializers.BooleanField()
    outlet = serializers.IntegerField()
    outs = OutsSerializer(many=True)


    def validate(self, attrs):
        return super().validate(attrs)
    # def to_representation(self, instance):
    #     return ResponseSerializer(instance, context=self.context).data
