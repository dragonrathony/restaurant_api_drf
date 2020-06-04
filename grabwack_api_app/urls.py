from django.urls import path
from django.conf.urls import include
from grabwack_api_app import apis
from grabwack_api_app import views
from rest_framework.authtoken import views as authviews

urlpatterns = [
    path('ping/', views.PingPong.as_view(), name='ping'),

    path('api-token-auth/', authviews.obtain_auth_token, name='api-tokn-auth'),

    path('restaurant/list/', apis.get_all_restaurants),

    path('restaurant/meals/list/<int:restaurant_id>/', apis.get_restaurant_meals),

#    path('restaurant/orders/list/<int:restaurant_id>/', apis.get_restaurant_orders),

    path('restaurant/reports/', apis.get_restaurant_reports),

    path('customer/meals/order/add/', apis.customer_add_order),

    path('customer/meals/order/latest/', apis.customer_latest_order),

    path('customer/driver/location/', apis.customer_driver_location),

    # Sign In/ Sign Up/ Sign Out
    path('social/', include('rest_framework_social_oauth2.urls')),

    # APIs for restaurant order notification
    path('restaurant/order/notification/<last_request_time>/', apis.restaurant_order_notification),

    # APIs for DRIVERS
    path('driver/orders/ready/', apis.driver_get_ready_orders),

    path('driver/order/pick/', apis.driver_pick_order),

    path('driver/order/latest/', apis.driver_get_latest_order),

    path('driver/order/complete/', apis.driver_complete_order),

    path('driver/revenue/', apis.driver_get_revenue),

    path('driver/location/update/', apis.driver_update_location),

    # Driver APIs
    path('driver/registration/', apis.driver_registration),

    path('driver/api-token-auth/', apis.driver_login),

    path('restaurant/registration/', apis.registration),

    path('restaurant/login/', apis.login),

    path('restaurant/updateProfile/', apis.update_profile),

    path('restaurant/create_meals/', apis.create_meals),

    path('restaurant/update_meals/<int:meal_id>', apis.update_meals),

    path('restaurant/restaurant_meals/<int:restaurant_id>/', apis.restaurant_meals),

    path('restaurant/restaurant_orders/<int:restaurant_id>/', apis.restaurant_orders),

    path('restaurant/orders/ready/', apis.set_ready_orders),

]
