from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboards
    path("dashboard/oem/", views.oem_dashboard, name="oem_dashboard"),
    path("dashboard/technician/", views.technician_dashboard, name="technician_dashboard"),

    # Service Requests (OEM)
    path("service-request/create/", views.create_service_request, name="create_service_request"),

    # Job Listings & Applications (Technicians)
    path("jobs/", views.job_list, name="job_list"),
    path("jobs/<int:pk>/apply/", views.apply_for_job, name="apply_for_job"),
    path("jobs/<int:pk>/confirm/", views.confirm_job, name="confirm_job"),
    path("jobs/<int:pk>/complete/", views.complete_job, name="complete_job"),
    path("service-request/<int:id>/edit/", views.edit_service_request, name="edit_service_request"),
    # Reviews
    path("reviews/<int:pk>/", views.leave_review, name="leave_review"),
]
