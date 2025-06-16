# orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('bulk/', views.bulk_order, name='bulk_order'),
]
