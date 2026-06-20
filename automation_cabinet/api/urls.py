
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import AutomatViewSet, generate

router = DefaultRouter()
router.register('test', AutomatViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('test/', generate),
]