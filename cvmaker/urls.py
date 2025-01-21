from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path("", views.cvmaker, name='cvmaker'),
    path("form/",views.form, name='form'),
    path("cv/", views.cv_view, name="cv_view"),

]
