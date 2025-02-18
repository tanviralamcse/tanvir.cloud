from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.urls import reverse
from decimal import Decimal, InvalidOperation
from .forms import JobApplicationForm  # Add this import


from oem.forms import CustomUserCreationForm, ServiceRequestForm, TechnicianApplicationForm
from .models import Job, ServiceRequest, JobApplication, JobExecution, Review, Technician, TechnicianApplication

User = get_user_model()

# Homepage
def homepage(request):
    return render(request, 'homepage.html')

# Register View
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.role = form.cleaned_data['role']
            user.save()
            login(request, user)
            return redirect("oem_dashboard" if user.role == "OEM" else "technician_dashboard")
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("oem_dashboard" if user.role == "OEM" else "technician_dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

# Logout View
def logout_view(request):
    response = redirect("login")
    response["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    logout(request)
    return response

# OEM Dashboard
@login_required
def oem_dashboard(request):
    if request.user.role != "OEM":
        return redirect("technician_dashboard")

    service_requests = ServiceRequest.objects.filter(oem=request.user)
    return render(request, "oem_dashboard.html", {"service_requests": service_requests})

# Technician Dashboard
@login_required
def technician_dashboard(request):
    applied_jobs = JobApplication.objects.filter(technician=request.user)
    return render(request, "technician_dashboard.html", {"applied_jobs": applied_jobs})

# Job Listings
@login_required
def job_list(request):
    jobs = ServiceRequest.objects.filter(status="open").order_by("-created_at")
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "job_list.html", {"page_obj": page_obj})


@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(ServiceRequest, id=job_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.technician = request.user
            application.request = job
            application.save()

            # Add a success message
            messages.success(request, "Application submitted successfully!")

            # Redirect to the jobs list page
            return redirect("job_list")
    
    else:
        form = JobApplicationForm()

    return render(request, "apply_for_job.html", {"form": form, "job": job})


# Confirm Job
@login_required
def confirm_job(request, job_id):
    job_application = get_object_or_404(JobApplication, id=job_id)

    if request.user == job_application.request.oem:
        job_application.status = "Confirmed"
        job_application.save()
        return redirect("oem_dashboard")

# Complete Job
@login_required
def complete_job(request, job_id):
    job_execution = get_object_or_404(JobExecution, id=job_id)

    if request.method == "POST":
        job_execution.service_report = request.POST["service_report"]
        job_execution.status = "Completed"
        job_execution.save()
        return redirect("technician_dashboard")

    return render(request, "complete_job.html", {"job_execution": job_execution})

# Leave Review
@login_required
def leave_review(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        Review.objects.create(
            reviewer=request.user,
            reviewed_user=job.technician,
            rating=request.POST["rating"],
            comments=request.POST["comments"]
        )
        return redirect("dashboard")

    return render(request, "leave_review.html", {"job": job})

# Edit Service Request
@login_required
def edit_service_request(request, job_id):
    service_request = get_object_or_404(ServiceRequest, id=job_id, oem=request.user)

    if request.method == "POST":
        form = ServiceRequestForm(request.POST, instance=service_request)
        if form.is_valid():
            form.save()
            return redirect("oem_dashboard")

    return render(request, "edit_service_request.html", {"form": form})

@login_required
def job_applicants(request, job_id):
    job = get_object_or_404(ServiceRequest, id=job_id, oem=request.user)
    applicants = JobApplication.objects.filter(request=job)  # Fix: Use `request=job`

    return render(request, "job_applicants.html", {"job": job, "applicants": applicants})



@login_required
def create_service_request(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        machine_details = request.POST["machine_details"]
        service_type = request.POST["service_type"]
        budget = request.POST["budget"]
        
        # Add validation here
        if not title or not description or not machine_details or not service_type or not budget:
            return render(request, "service_request_form.html", {"error": "All fields are required."})
        
        ServiceRequest.objects.create(
            oem=request.user,
            title=title,
            description=description,
            machine_details=machine_details,
            service_type=service_type,
            budget=budget,
            status="Open"
        )
        return redirect("dashboard")  # Redirect to dashboard after submitting the request
    return render(request, "service_request_form.html")

@login_required
def hire_technician(request, job_id, technician_id):
    job = get_object_or_404(Job, id=job_id)
    technician = get_object_or_404(User, id=technician_id)

    if request.user != job.oem_user:
        messages.error(request, "You are not authorized to hire for this job.")
        return redirect("job_list")

    job.hired_technician = technician
    job.status = "ongoing"
    job.applied_technicians.clear()
    job.save()
    messages.success(request, f"{technician.username} has been hired!")

    return redirect("job_list")

@login_required
def end_contract(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user != job.oem_user:
        messages.error(request, "You are not authorized to end this contract.")
        return redirect("job_list")

    job.status = "completed"
    job.save()
    messages.success(request, "The contract has been successfully ended!")

    return redirect("job_list")

@login_required
def ongoing_jobs(request):
    if request.user.groups.filter(name='OEM').exists():
        jobs = Job.objects.filter(oem_user=request.user, status="ongoing")
    else:
        jobs = Job.objects.filter(hired_technician=request.user, status="ongoing")

    return render(request, "ongoing_jobs.html", {"jobs": jobs})


@login_required
def applied_jobs(request):
    applied_jobs_list = JobApplication.objects.filter(user=request.user)  # Get jobs applied by the logged-in user
    return render(request, "oem/applied_jobs.html", {"applied_jobs": applied_jobs_list})