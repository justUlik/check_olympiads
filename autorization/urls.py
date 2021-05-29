"""
Assigning links for
external access to views.py functions
"""
from django.urls import path
from .views import login_view, logout_view, register_view, profile_view

urlpatterns = [
    path('signin/', login_view),
    path('logout/', logout_view),
    path('signup/', register_view),
    path('profile/', profile_view)
]
