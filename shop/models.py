from timeit import default_number
from django import forms
from django.db import models
from phone_field import PhoneField

# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = PhoneField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class WorkOrders(models.Model):
    PRICE = (
        (120, "MOUNTBALANCE"),
        (60, "TIRESWAP"),
    )
    work_title = models.CharField(max_length=30)
    work_body = models.TextField()
    phone_number = PhoneField()
    pricing = models.FloatField(choices=PRICE, default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.work_title
