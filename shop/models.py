from django.db import models
from phone_field import PhoneField

# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = PhoneField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"