from django.urls import path
from . import views
from .view import stockView

urlpatterns = [
    path('', views.index, name='index'),
    path('view', stockView.stock, name='stock')
]