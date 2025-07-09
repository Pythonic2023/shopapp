from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("customers/", views.create_customer, name="customers"),
    path("workorders/", views.work_orders, name="workorders"),
    path("error/", views.site_error, name="error"),
    path("customerdetail/", views.customer_detail, name="customerdetail"),
]