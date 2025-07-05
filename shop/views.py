from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Customer
from .forms import CustomerForm


# Create your views here.


# Goes to main page
def index(request):
    return render(request, "shop/index.html", {})


# Loads form, or submits form creates customer if number in database is not existent
def create_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            try:
                phone_number_obj = form.cleaned_data['phone_number']
                phone_number_str = str(phone_number_obj)
                raw_number = ''.join(char for char in phone_number_str if char.isdigit())
                phone_number_int = int(raw_number)
                if isinstance(phone_number_int, int):
                    customer_name = form.cleaned_data['first_name']
                    print(customer_name)
                    form.save(commit=False)
                    try:
                        get_customer = Customer.objects.get(phone_number=phone_number_str)
                        if get_customer:
                            error = "Phone number exists"
                            return site_error(request, error)
                    except ObjectDoesNotExist:
                        form.save()
                    customer = Customer.objects.get(phone_number=phone_number_str)
                    customer_pk = customer.pk
                    return customer_detail(request, customer_pk)
            except ValueError:
                error = "ERROR: Please type your number again with only digits."
                return site_error(request, error)

        else:
            return redirect(reverse("index"))
    else:
        form = CustomerForm()
        context = {'form': form}
        return render(request, "shop/customers.html", context)

# Shows error on page
def site_error(request, site_error):
    error_message = site_error
    context = {'error_message': error_message}
    return render(request, "shop/siteerror.html", context)

# Renders page with customer name
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer_name = customer.first_name
    context = {
        'customer_name': customer_name,
    }
    return render(request, "shop/customerdetail.html", context)

