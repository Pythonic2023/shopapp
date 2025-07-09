from django.forms import ModelForm
from .models import Customer

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number']


class PhoneForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number']
