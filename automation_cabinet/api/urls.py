
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import AutomatViewSet

router = DefaultRouter()
router.register('test', AutomatViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]