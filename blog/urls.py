from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.blog, name='blog'),
    path("user_login/", views.user_login, name='user_login'),
    path("logout/", views.custom_logout, name='logout'),
    path("signup/", views.signup, name='signup'),
    path("dashboard/", views.dashboard, name='dashboard'),  # Correct URL path
    path("svr/", views.svr, name = 'svr' ),
    path("g_svr/", views.g_svr, name = 'g_svr' )
]




