from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from .views import main

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main, name="main"),
]


