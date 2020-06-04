
from django.contrib import admin
from django.urls import path
from grabwack_customers_app import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('account', views.customer_home, name = 'customer-home'),

    path('sign-in/', auth_views.LoginView.as_view
        (template_name= 'customer/sign-in.html'),
        name = 'customer-sign-in'),

    path('sign-out', auth_views.LogoutView.as_view
        (next_page= 'customer/sign-in.html'),
        name = 'customer-sign-out'),

    path('sign-up', views.customer_sign_up,
        name = 'customer-sign-up'),

]
