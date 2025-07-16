from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from phone_field.templatetags.phone import raw_phone

from .models import Customer, WorkOrders
from .forms import CustomerForm, PhoneForm, WorkOrdersForm, RemoveOrderForm


# Create your views here.


# Goes to main page
def index(request):
    return render(request, "shop/index.html", {})


# Loads form, or submits form creates customer if number in database is not existent
def create_customer(request):
    if request.method == "POST":
        form_customer_create = CustomerForm(request.POST, prefix="form_customer_create")
        form_customer_search = PhoneForm(request.POST, prefix="form_customer_search")
        print(request.POST)
        if form_customer_create.is_valid():
            return add_customer(request, form_customer_create)
        elif form_customer_search.is_valid():
            return search_customer(request, form_customer_search)
        else:
            error = "Form not valid"
            return site_error(request, error)
    else:
        form_customer_create = CustomerForm(prefix="form_customer_create")
        form_customer_search = PhoneForm(prefix="form_customer_search")
        context = {'form_customer_create': form_customer_create,
                   'form_customer_search': form_customer_search,
                   }
        return render(request, "shop/customers.html", context)



# Shows error on page
def site_error(request, site_error):
    error_message = site_error
    context = {'error_message': error_message}
    return render(request, "shop/siteerror.html", context)

# Renders page with customer name
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    first_name = customer.first_name
    last_name = customer.last_name
    phone_number = customer.phone_number
    context = {
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number,
    }
    return render(request, "shop/customerdetail.html", context)


def search_customer(request, form):
    try:
        phone_obj = form.cleaned_data['phone_number']
        phone_obj_str = str(phone_obj)
        raw_phone = ''.join(char for char in phone_obj_str if char.isdigit())
        int_phone = int(raw_phone)
        if isinstance(int_phone, int):
            customer = Customer.objects.get(phone_number=phone_obj_str)
            customer_pk = customer.pk
            return customer_detail(request, customer_pk)
    except ValueError:
        error = "Failed"
        return site_error(request, error)

def add_customer(request, form):
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



def add_order(request):
    if request.method == "POST":
        work_order_create = WorkOrdersForm(request.POST)
        print(request.POST.get('phone_number_0'))
        if work_order_create.is_valid():
            phone_obj = work_order_create.cleaned_data['phone_number']
            phone_str = str(phone_obj)
            raw_number = ''.join(char for char in phone_str if char.isdigit())
            phone_int = int(raw_number)
            work_order_instance = work_order_create.save(commit=False)
            try:
                customer_obj = Customer.objects.get(phone_number=phone_str)
            except ObjectDoesNotExist:
                error = "Customer does not exist"
                return site_error(request, error)
            work_order_instance.customer = customer_obj
            if isinstance(phone_int, int):
                tax_percentage = 13
                price = work_order_instance.pricing
                price += (price * tax_percentage/100)
                work_order_instance.pricing = price
                work_order_instance.save()
            return redirect(reverse("workorders"))
        else:
            error = "Work order not valid"
            return site_error(request, error)
    else:
        work_order_create = WorkOrdersForm()
        context = {
            'work_order_create': work_order_create,
        }
        return render(request, "shop/addorder.html" ,context=context)



def work_orders(request):
    work_obj = WorkOrders.objects.all()
    context = {
        'work_obj': work_obj,
    }
    return render(request, "shop/workorders.html", context=context)


def remove_order(request):
    if request.method == "POST":
        remove_form = RemoveOrderForm(request.POST)
        if remove_form.is_valid():
            remove_form_id = remove_form.cleaned_data['id']
            try:
                order_instance = WorkOrders.objects.get(id=remove_form_id)
                order_instance.delete()
            except ObjectDoesNotExist:
                error = "Work order does not exist"
                site_error(request, error)
    else:
        remove_id = RemoveOrderForm()
        context = {
            'remove_id': remove_id,
        }
        return render(request, "shop/removeorder.html", context=context)
    return redirect(reverse("index"))