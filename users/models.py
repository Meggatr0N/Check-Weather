from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    city = models.CharField(max_length=150)
    units = models.CharField(max_length=150, default='celsius')