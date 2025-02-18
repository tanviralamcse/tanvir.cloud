import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from oem.models import ServiceRequest  # Adjust if your model has a different name

User = get_user_model()

class Command(BaseCommand):
    help = "Creates demo service requests for OEM users"

    def handle(self, *args, **kwargs):
        oem_users = User.objects.filter(role="oem")  # Fetch only OEM users

        if not oem_users.exists():
            self.stdout.write(self.style.WARNING("No OEM users found. Run 'create_demo_users' first."))
            return

        demo_requests = [
            "Fix motor issue",
            "Battery replacement",
            "Software update needed",
            "Sensor malfunction",
            "Routine maintenance",
        ]

        for oem in oem_users:
            for _ in range(random.randint(4, 5)):  # Create 4-5 requests per OEM
                service_request = ServiceRequest.objects.create(
                    oem=oem,
                    title=random.choice(demo_requests),
                    description="This is a test service request.",
                    status="pending",  # Adjust based on your model
                    budget=random.randint(500, 5000),  # Add a default budget
                )
                self.stdout.write(self.style.SUCCESS(f"Service request '{service_request.title}' created for {oem.username}."))

        self.stdout.write(self.style.SUCCESS("Demo service requests created successfully!"))

