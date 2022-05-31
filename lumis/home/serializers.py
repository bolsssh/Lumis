from django.core import serializers
from .models import *
data = serializers.serialize("json", Photo.objects.all())