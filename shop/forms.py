from email.policy import default

from django import forms
from django.forms import ModelForm
from .models import Customer, WorkOrders

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number']


class PhoneForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number']


class WorkOrdersForm(ModelForm):
    class Meta:
        model = WorkOrders
        fields = ['work_title', 'work_body', 'phone_number', 'pricing']


class RemoveOrderForm(forms.Form):
    order_number = forms.IntegerField(widget=forms.TextInput)
