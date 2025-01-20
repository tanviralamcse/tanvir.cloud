from django.urls import path, re_path, include
from . import views
urlpatterns = [
    path("", views.blog, name='blog'),
    path("login/", views.login, name = 'login'),
    path("signup/", views.signup, name = 'signup')
]


