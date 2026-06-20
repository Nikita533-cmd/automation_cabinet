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

from api.serializers import AutomatSerializer, RequestSerializer, ResponseSerializer

from elements.models import Automat


class AutomatViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с Automat."""

    queryset = Automat.objects.all()
    serializer_class = RequestSerializer
    pagination_class = None
    search_fields = ('name',)


@api_view(['POST'])
def generate(request):
    serializer = RequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    input_data = serializer.data
    print("Входные данные:", input_data)
    automat = get_object_or_404(Automat, i=40)
    generated_power = input_data['power'] * 1.5  # Ваша формула
    generated_count = input_data['count']
    generated_elements = []

    element = {
            'X': automat.A,
            'Y': automat.B,
            'Z': automat.C,
            'path': automat.Path
        }
    generated_elements.append(element)
    generated_elements.append(element)

    output_data = {
        'power': generated_power,
        'count': generated_count,
        'elements': generated_elements
    }
    print(output_data)
    response_serializer = ResponseSerializer(data=output_data)
    if not response_serializer.is_valid():
        return Response(response_serializer.errors, status= 403)
    return Response(response_serializer.data, status=200)