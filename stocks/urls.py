from django.urls import path
from . import views
from .view import stockView

urlpatterns = [
    path('', views.index, name='index'),
    path('search', stockView.divMethod, name='search'),
]