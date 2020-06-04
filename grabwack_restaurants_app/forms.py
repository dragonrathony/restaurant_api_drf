from django import forms
from django.contrib.auth.models import User
from grabwack_restaurants_app.models import Restaurant, Meal


class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email")


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ("restaurant_name", "restaurant_phone", "restaurant_address", "restaurant_location",  "cuisines",
                  "delivery_time", "mon_open_time", "tue_open_time", "wed_open_time", "thur_open_time", "fri_open_time",
                  "sat_open_time", "sun_open_time", "mon_close_time", "tue_close_time", "wed_close_time",
                  "thur_close_time", "fri_close_time","sat_close_time", "sun_close_time", "restaurant_logo")


class UserFormForEdit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        exclude = ("restaurant",)
