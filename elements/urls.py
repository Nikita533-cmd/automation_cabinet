from django.urls import path
from . import  views

urlpatterns = [
     path('', views.baseaup, name='baseaup'),
     path('test/', views.test),
     
]
