"""
Assigning links for
external access to views.py functions
"""
from django.urls import path
from .views import check_olympiad_info, register_to_olympiad

urlpatterns = [
    path('<str:olympiad_name>/', check_olympiad_info),
    path('<str:olympiad_name>/register_olympiad/', register_to_olympiad)
]
