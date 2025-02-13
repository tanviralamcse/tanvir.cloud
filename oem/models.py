
from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    ROLE_CHOICES = [
        ('OEM', 'OEM'),
        ('Technician', 'Technician'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username


# Technician Profile Model
class TechnicianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='technician_profile')
    skills = models.TextField()
    experience = models.IntegerField(help_text="Years of experience")
    service_regions = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.username

# Service Request Model
class ServiceRequest(models.Model):
    SERVICE_TYPES = [
        ('maintenance', 'Maintenance'),
        ('repair', 'Repair'),
        ('inspection', 'Inspection'),
        ('installation', 'Installation')
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    
    oem = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    title = models.CharField(max_length=255)
    description = models.TextField()
    machine_details = models.TextField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Job Application Model
class JobApplication(models.Model):
    technician = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField()
    price_offer = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.technician.username} applied for {self.request.title}"

# Job Execution Model
class JobExecution(models.Model):
    technician = models.ForeignKey(User, on_delete=models.CASCADE, related_name='executed_jobs')
    oem = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_jobs')
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE, related_name='execution')
    photos = models.ImageField(upload_to='job_photos/', blank=True, null=True)
    service_report = models.TextField()
    status = models.CharField(max_length=20, choices=[('ongoing', 'Ongoing'), ('completed', 'Completed')], default='ongoing')
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job Execution: {self.service_request.title}"

# Ratings & Reviews Model
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.IntegerField()
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewed_user.username}"
