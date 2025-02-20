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
    path('service-request/create/', views.create_service_request, name='create_service_request'),
    path("service-request/<int:job_id>/edit/", views.edit_service_request, name="edit_service_request"),

    # Job Listings & Applications (Technicians)
    path("jobs/", views.job_list, name="job_list"),
    path("jobs/<int:job_id>/apply/", views.apply_for_job, name="apply_for_job"),  # Application page
    path("jobs/<int:job_id>/confirm/", views.confirm_job, name="confirm_job"),
    path("jobs/<int:job_id>/complete/", views.complete_job, name="complete_job"),
    path("jobs/<int:job_id>/applicants/", views.job_applicants, name="job_applicants"),
    
    # Hiring & Contracting
    path("hire/<int:job_id>/<int:technician_id>/", views.hire_technician, name="hire_technician"),
    path("end_contract/<int:job_id>/", views.end_contract, name="end_contract"),
    
    # Reviews
    path("reviews/<int:job_id>/", views.leave_review, name="leave_review"),

    # Jobs Dashboard
    path("ongoing_jobs/", views.ongoing_jobs, name="ongoing_jobs"),
    path("applied_jobs/", views.applied_jobs, name="applied_jobs"),
]
