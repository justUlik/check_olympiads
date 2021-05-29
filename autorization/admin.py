"""
Providing accesses for DB at /admin
"""
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
