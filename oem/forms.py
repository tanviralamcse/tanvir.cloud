# oem/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import TechnicianApplication


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('OEM', 'OEM'),
        ('Technician', 'Technician'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="User Role")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

class TechnicianApplicationForm(forms.ModelForm):
    class Meta:
        model = TechnicianApplication
        fields = ['skills']

from django import forms
from .models import ServiceRequest

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ["title", "description", "status"]
