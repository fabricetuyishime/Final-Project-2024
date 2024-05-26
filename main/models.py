from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Sum

User = get_user_model()


# Create your models here.
class Fish(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    size = models.CharField(max_length=200, blank=True, null=True)
    age = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to="fish", blank=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Disease(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name
