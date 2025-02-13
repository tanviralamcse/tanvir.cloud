from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    
    # Service Requests (OEM)
    path("service-request/create/", views.create_service_request, name="create_service_request"),
    
    # Job Listings (Technicians)
    path("jobs/", views.job_listings, name="job_listings"),
    path("job/<int:id>/apply/", views.apply_for_job, name="apply_for_job"),
    path("job/<int:id>/confirm/", views.confirm_job, name="confirm_job"),
    path("job/<int:id>/complete/", views.complete_job, name="complete_job"),
    
    # Reviews
    path("review/<int:id>/", views.leave_review, name="leave_review"),
]
