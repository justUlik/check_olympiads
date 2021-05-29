"""
Providing accesses for DB at /admin
"""
from django.contrib import admin
from .models import Olympiad, registerOlympiad

admin.site.register(Olympiad)
admin.site.register(registerOlympiad)
