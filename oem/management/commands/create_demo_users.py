from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the correct User model

class Command(BaseCommand):
    help = "Creates demo OEMs and Technicians"

    def handle(self, *args, **kwargs):
        demo_users = [
            {"username": "oem1", "password": "password123", "role": "oem"},
            {"username": "oem2", "password": "password123", "role": "oem"},
            {"username": "tech1", "password": "password123", "role": "technician"},
            {"username": "tech2", "password": "password123", "role": "technician"},
            {"username": "oem3", "password": "password123", "role": "oem"},
            {"username": "tech3", "password": "password123", "role": "technician"},
        ]

        for user_data in demo_users:
            username = user_data["username"]
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=user_data["password"])
                user.role = user_data["role"]  # Set the role if your model has it
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User '{username}' created."))
            else:
                self.stdout.write(self.style.WARNING(f"User '{username}' already exists."))
