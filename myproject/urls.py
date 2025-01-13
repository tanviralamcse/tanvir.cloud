from django.contrib import admin
from django.urls import path, re_path
from .views import main

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main, name="main"),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)