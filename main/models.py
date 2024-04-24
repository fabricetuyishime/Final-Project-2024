from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Sum

User = get_user_model()


# Create your models here.
class Fish(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to="fish", blank=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name
