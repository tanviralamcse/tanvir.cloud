from django.contrib import admin
from django.urls import path, re_path
from .views import main

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main, name="main"),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]
