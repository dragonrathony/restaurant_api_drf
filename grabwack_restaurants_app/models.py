from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from grabwack_customers_app.models import Customer
from grabwack_drivers_app.models import Driver

# Create your models here.


class fcm_info(models.Model):
    fcm_token = models.CharField(max_length=400)
    def __str__(self):
        return self.fcm_token


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    restaurant_name = models.CharField(max_length=500, blank=False)
    restaurant_phone = models.CharField(max_length=500, blank=False)
    restaurant_address = models.CharField(max_length=500, blank=False)
    restaurant_location = models.CharField(max_length=500, blank=False)
    cuisines = models.CharField(max_length=500, blank=False)
    delivery_time = models.IntegerField(blank=True, null=True)
    mon_open_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    tue_open_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    wed_open_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    thur_open_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    fri_open_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    sat_open_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    sun_open_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    mon_close_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    tue_close_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    wed_close_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    thur_close_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    fri_close_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    sat_close_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    sun_close_time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    restaurant_logo = models.ImageField(upload_to='restaurant_logo/', blank=False)

    def __str__(self):
        return self.restaurant_name


class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant,  on_delete=models.CASCADE,)
    name = models.CharField(max_length=500)
    short_description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='meal_images/', blank=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    COOKING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (COOKING, "Cooking"),
        (READY, "Ready"),
        (ONTHEWAY, "On the way"),
        (DELIVERED, "Delivered"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True,)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    total = models.IntegerField()
    status = models.IntegerField(choices = STATUS_CHOICES)
    created_at = models.DateTimeField(default = timezone.now)
    picked_at = models.DateTimeField(blank = True, null=True)

    def __str__(self):
        return str(self.id)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_detail')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE,)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()

    def __str__(self):
        return str(self.id)
