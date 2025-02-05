from django.urls import path, re_path, include
from . import views
urlpatterns = [
    path("", views.blog, name='blog'),
    path("login/", views.login, name = 'login'),
    path("signup/", views.signup, name = 'signup'),
    path("svr/", views.svr, name = 'svr' ),
    path("g_svr/", views.g_svr, name = 'g_svr' )
]


