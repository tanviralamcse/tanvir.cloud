from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.urls import reverse
from .forms import JobApplicationForm  # Add this import
from django.urls import reverse


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

@login_required
def oem_dashboard(request):
    oem_jobs = ServiceRequest.objects.filter(oem=request.user)  # Ensure jobs exist
    oem_user = request.user
    job_applications = {}

    for job in oem_jobs:
        job_applications[job.id] = JobApplication.objects.filter(request=job)

    context = {
        "oem_jobs": oem_jobs,
        "job_applications": job_applications,
        "oem_user": oem_user,
    }

    return render(request, "oem_dashboard.html", context)


# Technician Dashboard
@login_required
def technician_dashboard(request):
    technician = request.user
    job_applications = JobApplication.objects.filter(technician=technician).select_related('request')
    return render(request, "technician_dashboard.html", {
        "technician": technician,  # Pass technician to template
        "job_applications": job_applications
    })

# Job Listings
@login_required
def job_list(request):
    alljobs = ServiceRequest.objects.all()
    jobs = alljobs.order_by("-created_at")
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "job_list.html", {
        "page_obj": page_obj,
        "jobs": jobs
        })


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
    # Fetch the job and ensure it's associated with the logged-in OEM user
    job = get_object_or_404(ServiceRequest, id=job_id, oem=request.user)
    
    # Fetch the applicants for this job (assuming `request` is the ForeignKey to ServiceRequest)
    applicants = JobApplication.objects.filter(request=job)
    
    # Optionally, you could also fetch additional info, like the total number of applicants
    total_applicants = applicants.count()

    # Render the template with the job details and applicants list
    return render(request, "job_applicants.html", {
        "job": job,
        "applicants": applicants,
        "total_applicants": total_applicants,  # Include the total number of applicants
    })



from django.shortcuts import redirect
from django.urls import reverse

@login_required
def create_service_request(request):
    if request.method == "POST":
        # Get form data with safe defaults
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        service_type = request.POST.get("service_type", "").strip()
        
        try:
            budget = float(request.POST.get("budget", 0))
        except ValueError:
            return render(request, "service_requests/create.html", {
                "error": "Please enter a valid budget amount.",
                "form_data": request.POST  # Return form data for re-population
            })

        # Validation
        if not all([title, description, service_type, budget > 0]):
            return render(request, "service_request_form.html", {
                "error": "All fields are required and budget must be greater than 0.",
                "form_data": request.POST
            })

        try:
            ServiceRequest.objects.create(
                oem=request.user,
                title=title,
                description=description,
                service_type=service_type,
                budget=budget,
                status="Open"
            )
            messages.success(request, "Service request created successfully!")
            return redirect(reverse("oem_dashboard"))
        except Exception as e:
            return render(request, "service_request_form.html", {
                "error": f"Error creating service request: {str(e)}",
                "form_data": request.POST
            })

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
    # Get all job applications for the logged-in user
    applied_jobs_list = JobApplication.objects.filter(technician=request.user)
    
    # Pass job details to the template, along with the job applications
    return render(request, "oem/applied_jobs.html", {"applied_jobs": applied_jobs_list})
