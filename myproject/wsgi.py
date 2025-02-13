import os
from dotenv import load_dotenv
load_dotenv()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

app = get_wsgi_application()
