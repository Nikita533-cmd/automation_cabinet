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

