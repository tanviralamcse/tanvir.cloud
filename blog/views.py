from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.models import User


def blog(request):
    return render(request, 'blog/blog.html')


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/admindashboard/')  # Redirect after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {"form": form})


@login_required(login_url='/user_login/')
def dashboard(request):
    if request.user.is_staff:  # Redirect admins to the admin dashboard
        return redirect('/admin_dashboard/')
    
    return render(request, 'userPanel/user_dashboard.html', {'user': request.user})


@login_required(login_url='/user_login/')
def admin_dashboard(request):
    users = User.objects.all()  # Get all users
    return render(request, 'adminPanel/admin_dashboard.html', {"users": users})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log in the user automatically
            return redirect('/dashboard/')  # Redirect after signup
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {"form": form})


def custom_logout(request):
    logout(request)
    return redirect('/user_login/')


def svr(request):
    return render(request, 'svr/svr.html')


def g_svr(request):
    if request.method == 'POST':
        date_time = request.POST.get('dateTime')  # Get dateTime from the form

        if date_time:
            date_part, time_part = date_time.split("T")  # Splits into ["YYYY-MM-DD", "HH:MM"]
        else:
            date_part, time_part = None, None  # Handle missing value

        context = {
            "requestId": request.POST.get('requestId'),
            "clientId": request.POST.get('clientId'),
            "customerName": request.POST.get('customerName'),
            "siteName": request.POST.get('siteName'),
            "dateTime": date_time,
            "date": date_part,
            "time": time_part,
            "siteAddress": request.POST.get('siteAddress'),
            "localContact": request.POST.get('localContact'),
            "phoneNumber": request.POST.get('phoneNumber'),
            "partNumber": request.POST.get('partNumber'),
            "serialNumber": request.POST.get('serialNumber'),
            "comments": request.POST.get('comments')
            
        }

        return render(request, 'svr/g_svr.html', context)

    return render(request, 'svr/svr.html')  # Render default template if not POST request
