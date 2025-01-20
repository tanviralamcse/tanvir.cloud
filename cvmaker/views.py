from django.shortcuts import render

# Create your views here.
def cvmaker(request):
    return render(request, 'htmlfiles/base.html')

def form(request):
    return render(request, 'htmlfiles/form.html')