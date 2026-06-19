"""ViewSet'ы для API."""
import uuid

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.serializers import AutomatSerializer

from elements.models import Automat


class AutomatViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с Automat."""

    queryset = Automat.objects.all()
    serializer_class = AutomatSerializer
    pagination_class = None
    search_fields = ('name',)
