from django.db import models
from django.contrib.auth.models import User

class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default="Unknown Address")
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], default='male')  # Default to 'male'

    def __str__(self):
        return self.user.username
