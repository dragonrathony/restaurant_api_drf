
from rest_framework import serializers
from grabwack_restaurants_app.models import Restaurant, Meal, Order, OrderDetail
from django.contrib.auth.models import User
from grabwack_customers_app.models import Customer
from grabwack_drivers_app.models import Driver


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')


class RestaurantRegisterSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ("id", "restaurant_name", "restaurant_phone", "restaurant_address", "restaurant_location", "cuisines", "delivery_time", "logo", "fcm_token",
                  "mon_open_time", "tue_open_time", "wed_open_time", "thur_open_time", "fri_open_time", "sat_open_time", "sun_open_time",
                  "mon_close_time", "tue_close_time", "wed_close_time", "thur_close_time", "fri_close_time", "sat_close_time", "sun_close_time")


class RestaurantSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, restaurant):
        request = self.context.get('request')
        logo_url = restaurant.restaurant_logo.url
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Restaurant
        fields = ("id", "user", "restaurant_name", "restaurant_phone", "restaurant_address", "restaurant_location",
                  "cuisines", "delivery_time", "mon_open_time", "tue_open_time", "wed_open_time", "thur_open_time",
                  "fri_open_time", "sat_open_time", "sun_open_time", "mon_close_time", "tue_close_time",
                  "wed_close_time", "thur_close_time", "fri_close_time", "sat_close_time",
                  "sun_close_time", "logo")


class MealAddSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = ("id", "name", "short_description", "image", "price")


class MealSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    total_order = serializers.IntegerField()

    def get_image(self, meal):
        request = self.context.get('request')
        image_url = meal.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Meal
        fields = ("id", "name", "short_description", "image", "price", "total_order")


# ORDER SERIALIZER
class OrderCustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Customer
        fields = ("id", "name", "avatar", "phone", "address")


class DriverRegistrationSerializer(serializers.ModelSerializer):
    # name = serializers.ReadOnlyField(source="user.get_full_name")
    # name = serializers.SerializerMethodField()
    # avatar = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = ("id", "avatar", "phone", "address", "location")

    # def create(self, validated_data):
    #     return Driver.objects.create(**validated_data)

    # def get_avatar(self, driver):
    #     request = self.context.get('request')
    #     logo_url = driver.avatar.url
    #     return request.build_absolute_uri(logo_url)


class OrderDriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Driver
        fields = ("id", "name", "avatar", "phone", "address")


class OrderRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "restaurant_name", "restaurant_phone", "restaurant_address")


class OrderMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ("id", "name", "price")


class OrderDetailSerializer(serializers.ModelSerializer):
    meal = OrderMealSerializer()

    class Meta:
        model = OrderDetail
        fields = ("id", "meal", "quantity", "sub_total")


class OrderSerializer(serializers.ModelSerializer):
    customer = OrderCustomerSerializer()
    driver = OrderDriverSerializer()
    restaurant = OrderRestaurantSerializer()
    order_detail = OrderDetailSerializer(many = True)
    status = serializers.ReadOnlyField(source = "get_status_display")

    class Meta:
        model = Order
#        fields = ("id", "customer", "restaurant", "driver", "order_detail", "total", "status", "address_line_1")
        fields = ("id", "customer", "restaurant", "driver", "order_detail", "total", "status", "address", "name")
