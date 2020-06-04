from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from grabwack_customers_app.forms import UserForm, CustomerForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


@login_required(login_url='sign-in/')
def customer_home(request):
    return render(request, 'customer/customer_home.html', {})


def customer_sign_up(request):
    user_form = UserForm()
    customer_form = CustomerForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        customer_form = CustomerForm(request.POST, request.FILES)

        if user_form.is_valid() and customer_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_customer = customer_form.save(commit=False)
            new_customer.user = new_user
            new_customer.save()

            login(request, authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(customer_home)

    return render(request, 'customer/sign-up.html', {
        "user_form": user_form,
        "customer_form": customer_form
    })
