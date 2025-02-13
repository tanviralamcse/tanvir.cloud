from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # Blog Home
    path("", views.blog, name='blog'),

    # Authentication Routes
    path("user_login/", views.user_login, name='user_login'),
    path("logout/", views.custom_logout, name='logout'),
    path("signup/", views.signup, name='signup'),

    # Dashboard Routing
    path("dashboard/", views.dashboard, name='dashboard'),
    path("admin_dashboard/", views.admin_dashboard, name='admin_dashboard'),  # New admin route

    # Service Views
    path("svr/", views.svr, name='svr'),
    path("g_svr/", views.g_svr, name='g_svr'),

    # Django Admin Panel
]
