from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login


def blog(request):
    return render(request, 'blog/blog.html')

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/blog/dashboard/')  # Redirect after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {"form": form})


@login_required(login_url='/blog/user_login/')
def dashboard(request):
    print("User:", request.user)  # Should print the logged-in user's info
    context = {'user' : request.user}
    return render(request, "registration/admin.html", context)

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log in the user automatically
            return redirect('/blog/dashboard/')  # Redirect after successful signup
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {"form": form})


def custom_logout(request):
    logout(request)
    return redirect('/blog/user_login')

def svr(request):
    return render(request, 'svr/svr.html')

def g_svr(request):
    if request.method == 'POST':
        date_time = request.POST.get('dateTime')  # Get dateTime from the form
        
        if date_time:
            date_part, time_part = date_time.split("T")  # Splits into ["YYYY-MM-DD", "HH:MM"]
        else:
            date_part, time_part = None, None  # Handle missing value

        # Extract personal information from POST request
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
            "serialNumber": request.POST.get('serialNumber')
        }

        return render(request, 'svr/g_svr.html', context)  # Pass context to template

    return render(request, 'svr/svr.html')  # Render default template if not POST request
