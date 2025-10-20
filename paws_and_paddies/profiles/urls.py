from django.urls import path
from . import views

urlpatterns = [
    path('paws/', views.PawProfileList.as_view(), name='paw-list'),
]

