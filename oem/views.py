from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.contrib.auth import login

from oem.forms import CustomUserCreationForm

from .models import ServiceRequest, JobApplication, JobExecution, Review


# Homepage
def homepage(request):
    return render(request, 'homepage.html')


# Register View
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            user_role = form.cleaned_data['role']  # Get the role selected by the user
            user.role = user_role  # Assign the role to the user
            user.save()  # Save the user with the role

            login(request, user)  # Log the user in after registration
            return redirect("dashboard")  # Redirect to dashboard after registration
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)  # Use AuthenticationForm
        if form.is_valid():
            user = form.get_user()  # Get the authenticated user
            login(request, user)  # Log the user in

            # Redirect based on user role
            if user.role == "OEM":
                return redirect("dashboard")  # OEM Dashboard
            elif user.role == "Technician":
                return redirect("dashboard")  # Technician Dashboard
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})  # Handle form errors
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})  # Pass the form to the template

# Logout View
def logout_view(request):
    response = redirect("login")
    response["Cache-Control"] = "no-store, no-cache, must-revalidate"  # Prevent caching of the page
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    logout(request)  # Log out the user
    return response


@login_required
@never_cache  # Prevents caching for security
def dashboard(request):
    user = request.user  # Get logged-in user
    role = getattr(user, "role", None)  # Ensure role is safely accessed
    
    # Base context with user and role
    context = {
        "user": user,
        "role": role,
        "service_requests": None,
        "job_executions": None,
        "job_applications": None
    }

    # Fetch data based on role
    if role == "OEM":
        context.update({
            "service_requests": ServiceRequest.objects.filter(oem=user),
            "job_executions": JobExecution.objects.filter(oem=user)
        })
    elif role == "Technician":
        context["job_applications"] = JobApplication.objects.filter(technician=user)
    
    return render(request, "dashboard.html", context)

# 📋 Job Listings Page (Technicians view available jobs)
@login_required
def job_listings(request):
    jobs = ServiceRequest.objects.filter(status="Open")  # Get open jobs
    return render(request, "job_listings.html", {"jobs": jobs})


# 📝 Apply for a Job (Technician applies)
@login_required
def apply_for_job(request, id):
    job = get_object_or_404(ServiceRequest, id=id)
    
    if request.method == "POST":
        message = request.POST["message"]
        price_offer = request.POST["price_offer"]
        
        JobApplication.objects.create(
            technician=request.user,
            request=job,
            message=message,
            price_offer=price_offer,
            status="Pending"
        )
        return redirect("dashboard")  # Redirect to dashboard after applying for the job

    return render(request, "apply_for_job.html", {"job": job})


# ✅ Confirm Job (OEM selects technician)
@login_required
def confirm_job(request, id):
    job_application = get_object_or_404(JobApplication, id=id)
    
    if request.user == job_application.request.oem:  # Ensure the user is the OEM of the service request
        job_application.status = "Confirmed"
        job_application.save()
        return redirect("dashboard")  # Redirect after confirming the job


# 🔧 Complete Job (Technician uploads report)
@login_required
def complete_job(request, id):
    job_execution = get_object_or_404(JobExecution, id=id)
    
    if request.method == "POST":
        service_report = request.POST["service_report"]
        job_execution.service_report = service_report
        job_execution.status = "Completed"
        job_execution.save()
        return redirect("dashboard")  # Redirect after completing the job
    
    return render(request, "complete_job.html", {"job_execution": job_execution})


# ⭐ Leave Review (OEM or Technician leaves a review)
@login_required
def leave_review(request, id):
    reviewed_user = get_object_or_404(User, id=id)

    if request.method == "POST":
        rating = request.POST["rating"]
        comments = request.POST["comments"]

        Review.objects.create(
            reviewer=request.user,
            reviewed_user=reviewed_user,
            rating=rating,
            comments=comments
        )
        return redirect("dashboard")  # Redirect after leaving the review

    return render(request, "leave_review.html", {"reviewed_user": reviewed_user})


# 🛠️ Service Request Form (OEM submits a new service request)
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


# Homepage
def homepage(request):
    return render(request, 'homepage.html')

