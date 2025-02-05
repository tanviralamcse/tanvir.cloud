from django.shortcuts import render

def blog(request):
    return render(request, 'blog/blog.html')

def login(request):
    return render(request, 'login/login.html')

def signup(request):
    return render(request, 'signup/signup.html')

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
