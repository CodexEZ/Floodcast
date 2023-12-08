import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
import django
from shapely import Point ,Polygon
django.setup()

from api.models import Users

users = Users.objects.all()

for user in users:
    