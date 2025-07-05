from django.forms import ModelForm
from .models import Customer
from django.core.exceptions import ValidationError

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number']
