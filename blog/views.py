from django.shortcuts import render

def blog(request):
    return render(request, 'blog/blog.html')

def login(request):
    return render(request, 'login/login.html')

def signup(request):
    return render(request, 'signup/signup.html')