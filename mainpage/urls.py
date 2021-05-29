"""
Assigning links for
external access to views.py functions
"""
from django.urls import path
from .views import view_olympiads

urlpatterns = [
    path('', view_olympiads)
]
