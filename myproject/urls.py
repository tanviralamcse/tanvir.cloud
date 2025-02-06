from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from .views import main

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main, name="main"),
    path("__reload__/", include("django_browser_reload.urls")),
    path("blog/", include("blog.urls")),
    path("cvmaker/", include('cvmaker.urls') )
]


