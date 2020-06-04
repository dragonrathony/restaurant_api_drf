from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
import json
import os
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse, QueryDict
from rest_framework.authtoken.models import Token
from oauth2_provider.models import AccessToken
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from grabwack_restaurants_app.models import Restaurant, Meal, Order, OrderDetail
from grabwack_drivers_app.models import Driver
from django.contrib.auth.models import User
from grabwack_api_app.serializers import RestaurantSerializer, MealSerializer, OrderSerializer, UserSerializer, \
    RestaurantRegisterSerializer, MealAddSerializer, DriverRegistrationSerializer
from django.db.models import Sum, Count, Case, When
import stripe
from grabwack_restaurants.settings import STRIPE_API_KEY
stripe.api_key = STRIPE_API_KEY


@csrf_exempt
# API for registration restaurant
def registration(request):
    if request.method == "POST":

        serializer = UserSerializer(data=request.POST)
        restaurant_serializer = RestaurantRegisterSerializer(data=request.POST)

        if serializer.is_valid() and restaurant_serializer.is_valid():
            if len(request.FILES) == 0:
                return JsonResponse({"payload": {}, "status": "false",
                                     "response": "Please select restaurant logo"})
            else:
                f = request.FILES['restaurant_logo']
                file_path = os.path.join(os.getcwd(), 'media/restaurant_logo/')
                fs = FileSystemStorage(location=file_path)
                filename = fs.save(f.name, f)
                image_url = 'restaurant_logo/' + filename

            enc_password = make_password(request.POST['password'])
            user = serializer.save(password=enc_password)
            token = Token.objects.create(user=user).key

            if user:
                restaurant = restaurant_serializer.save(
                    user_id=user.id,
                    restaurant_logo=image_url
                )
                if restaurant:
                    restaurant = RestaurantSerializer(
                        Restaurant.objects.filter(user=user.id),
                        many=True,
                        context={"request": request}
                    ).data

                    user = UserSerializer(
                        User.objects.filter(id=user.id),
                        many=True,
                        context={"request": request}
                    ).data

                    return JsonResponse({"payload": {"token": token, "user": user[0], "restaurant": restaurant[0]},
                                         "status": "true", "response": "Success"})
                else:
                    return JsonResponse({"payload": {}, "status": "false",
                                         "response": restaurant_serializer.errors})
            else:
                return JsonResponse({"payload": {}, "status": "false", "response": serializer.errors})

        return JsonResponse({"payload": {}, "status": "false", "response": serializer.errors['username'][0]})


@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    if username is None or password is None:
        return JsonResponse({"payload": {}, "status": "false", "response": "Please input username and password"})

    user = authenticate(username=username, password=password)
    # status.HTTP_404_NOT_FOUND
    if not user:
        return JsonResponse({"payload": {}, "status": "false", "response": "Invalid credentials"})

    token, _ = Token.objects.get_or_create(user=user)

    # re = Restaurant.objects.get(user=user.id)
    # print(type(re))

    restaurant = RestaurantSerializer(
        Restaurant.objects.filter(user=user.id),
        many=True,
        context={"request": request}
    ).data

    user = UserSerializer(
        User.objects.filter(id=user.id),
        many=True,
        context={"request": request}
    ).data

    # status.HTTP_200_OK
    return JsonResponse({"payload": {"token": token.key, "user": user[0], "restaurant": restaurant[0]},
                         "status": "true", "response": "Success"})


def match_restaurant(request, key_objects, restaurant):
    restaurant.restaurant_name = key_objects[0]
    restaurant.restaurant_phone = key_objects[1]
    restaurant.restaurant_address = key_objects[2]
    restaurant.restaurant_location = key_objects[3]
    restaurant.cuisines = key_objects[4]
    restaurant.delivery_time = key_objects[5]
    restaurant.mon_open_time = key_objects[6]
    restaurant.tue_open_time = key_objects[7]
    restaurant.wed_open_time = key_objects[8]
    restaurant.thur_open_time = key_objects[9]
    restaurant.fri_open_time = key_objects[10]
    restaurant.sat_open_time = key_objects[11]
    restaurant.sun_open_time = key_objects[12]
    restaurant.mon_close_time = key_objects[13]
    restaurant.tue_close_time = key_objects[14]
    restaurant.wed_close_time = key_objects[15]
    restaurant.thur_close_time = key_objects[16]
    restaurant.fri_close_time = key_objects[17]
    restaurant.sat_close_time = key_objects[18]
    restaurant.sun_close_time = key_objects[19]
    try:
        f = request.FILES['restaurant_logo']
        file_path = os.path.join(os.getcwd(), 'media/restaurant_logo/')
        fs = FileSystemStorage(location=file_path)
        old_path = restaurant.restaurant_logo.path
        if(os.path.exists(old_path)):
            os.remove(old_path)
        filename = fs.save(f.name, f)
        image_url = 'restaurant_logo/' + filename
        restaurant.restaurant_logo.name = image_url

    except Exception as e:
        print(e)
        pass
    return restaurant

# Update Profile
@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        token = request.META['HTTP_AUTHORIZATION']
        user = Token.objects.get(key=token).user
        restaurant = Restaurant.objects.get(user_id=user.id)
        origin_username = user.username

        try:
            user.username = request.POST['username']
        except Exception as e:
            user.username = origin_username
            print(e)
        else:
            try:
                User.objects.get(username=request.POST['username'])
                if origin_username == request.POST['username']:
                    pass
                else:
                    return JsonResponse({"payload": {}, "status": "false", "response": "Username is already exist"})
            except Exception as e:
                print(e)
                pass
        try:
            enc_password = make_password(request.POST['password'])
            user.password = enc_password
        except Exception as e:
            print(e)
            pass
        try:
            user.email = request.POST['email']
        except Exception as e:
            print(e)
            pass
        try:
            user.first_name = request.POST['first_name']
        except Exception as e:
            print(e)
            pass
        try:
            user.last_name = request.POST['last_name']
        except Exception as e:
            print(e)
            pass

        key_str = ["restaurant_name", "restaurant_phone", "restaurant_address", "restaurant_location", "cuisines",
                   "delivery_time", "mon_open_time", "tue_open_time", "wed_open_time", "thur_open_time",
                   "fri_open_time", "sat_open_time", "sun_open_time", "mon_close_time", "tue_close_time",
                   "wed_close_time", "thur_close_time", "fri_close_time", "sat_close_time", "sun_close_time"]
        key_objects = [restaurant.restaurant_name, restaurant.restaurant_phone, restaurant.restaurant_address,
                       restaurant.restaurant_location, restaurant.cuisines, restaurant.delivery_time,
                       restaurant.mon_open_time, restaurant.tue_open_time, restaurant.wed_open_time,
                       restaurant.thur_open_time, restaurant.fri_open_time, restaurant.sat_open_time,
                       restaurant.sun_open_time, restaurant.mon_close_time, restaurant.tue_close_time,
                       restaurant.wed_close_time, restaurant.thur_close_time, restaurant.fri_close_time,
                       restaurant.sat_close_time, restaurant.sun_close_time]

        for i in range(len(key_str)):
            try:
                key_objects[i] = request.POST[key_str[i]]
            except Exception as e:
                print(e)
                pass

        restaurant = match_restaurant(request, key_objects, restaurant)
        print(user.username)
        user.save()
        restaurant.save()

        restaurant = RestaurantSerializer(
            Restaurant.objects.filter(user=user.id),
            many=True,
            context={"request": request}
        ).data

        user = UserSerializer(
            User.objects.filter(id=user.id),
            many=True,
            context={"request": request}
        ).data

        return JsonResponse({"payload": {"token": token, "user": user[0], "restaurant": restaurant[0]},
                             "status": "true", "response": "Success"})

# Create meals
@csrf_exempt
def create_meals(request):
    if request.method == "POST":
        token = request.META['HTTP_AUTHORIZATION']
        user = Token.objects.get(key=token).user
        restaurant_id = user.restaurant.id

        serializer = MealAddSerializer(data=request.POST)
        if serializer.is_valid():
            try:
                f = request.FILES['image']
                file_path = os.path.join(os.getcwd(), 'media/meal_images/')
                fs = FileSystemStorage(location=file_path)
                filename = fs.save(f.name, f)
                image_url = 'meal_images/' + filename
            except Exception as e:
                print(e)
                return JsonResponse({"payload": {}, "status": "false",
                                     "response": "Please select image"})

            meal = serializer.save(
                restaurant_id=restaurant_id,
                image=image_url
            )

            if meal:
                meals = MealSerializer(
                    Meal.objects.filter(restaurant_id=restaurant_id).order_by("-id"),
                    many=True,
                    context={"request": request}
                ).data

                return JsonResponse({"payload": {"meals": meals}, "status": "true", "response": "Success"})
            else:
                return JsonResponse({"payload": {}, "status": "false", "response": serializer.errors})

        else:
            return JsonResponse({"payload": {}, "status": "false", "response": serializer.errors})

# Update meals
@csrf_exempt
def update_meals(request, meal_id):
    token = request.META['HTTP_AUTHORIZATION']
    user = Token.objects.get(key=token).user
    restaurant_id = user.restaurant.id

    if request.method == "POST":
        meals = Meal.objects.get(id=meal_id)
        if meals.restaurant_id != restaurant_id:
            return JsonResponse({"payload": {}, "status": "false", "response": "Invalid operation"})
        try:
            meals.name = request.POST['name']
        except Exception as e:
            print(e)
            pass
        try:
            meals.short_description = request.POST['short_description']
        except Exception as e:
            print(e)
            pass
        try:
            meals.price = request.POST['price']
        except Exception as e:
            print(e)
            pass
        try:
            f = request.FILES['image']
            file_path = os.path.join(os.getcwd(), 'media/meal_images/')
            fs = FileSystemStorage(location=file_path)
            old_path = meals.image.path

            if(os.path.exists(old_path)):
                os.remove(old_path)
            filename = fs.save(f.name, f)
            image_url = 'meal_images/' + filename
            meals.image.name = image_url
        except Exception as e:
            print(e)
            pass

        meals.save()

        meal = MealSerializer(
            Meal.objects.filter(id=meal_id),
            many=True,
            context={"request": request}
        ).data

        return JsonResponse({"payload": {"meals": meal[0]}, "status": "true", "response": "Success"})


@csrf_exempt
# API for restaurant fetch meals
def restaurant_meals(request, restaurant_id):
    token = request.META['HTTP_AUTHORIZATION']
    user = Token.objects.get(key=token).user
    restaurant_id = user.restaurant.id

    meals = MealSerializer(
        Meal.objects.filter(restaurant_id = restaurant_id).order_by("-id"),
        many=True,
        context={"request": request}
    ).data
    return JsonResponse({"payload": {"meals": meals}, "status": "true", "response": "Success"})


@csrf_exempt
# API for restaurant order meals list
def restaurant_orders(request, restaurant_id):
    token = request.META['HTTP_AUTHORIZATION']
    user = Token.objects.get(key=token).user
    restaurant_id = user.restaurant.id

    orders = OrderSerializer(
        Order.objects.filter(restaurant_id = restaurant_id).order_by("-id"),
        many=True,
        context={"request": request}
    ).data
    return JsonResponse({"payload": {"orders": orders}, "status": "true", "response": "Success"})


@csrf_exempt
# POST params: access_token, order_id
def set_ready_orders(request):
    token = request.META['HTTP_AUTHORIZATION']
    user = Token.objects.get(key=token).user
    restaurant_id = user.restaurant.id
    if restaurant_id:
        order = Order.objects.get(id=request.POST["order_id"], driver=None)
        order.status = Order.READY
        order.save()

        orders = OrderSerializer(
            Order.objects.filter(restaurant_id = restaurant_id).order_by("-id"),
            many=True,
            context={"request": request}
        ).data
    return JsonResponse({"payload": {"orders": orders}, "status": "true", "response": "READY"})
    #return JsonResponse({"status": "success"})


##############
# CUSTOMERS
##############

# API for customer fetch restaurant
def get_all_restaurants(request):
    restaurants = RestaurantSerializer(
        Restaurant.objects.all().order_by("-id"),
        many=True,
        context={"request": request}
    ).data

    return JsonResponse({"restaurants": restaurants})

"""
# API for customer fetch meals
def get_restaurant_orders(request, restaurant_id):
    orders = OrderSerializer(
        Order.objects.filter(restaurant_id = restaurant_id).order_by("-id"),
        many=True,
        context={"request": request}
    ).data

    return JsonResponse({"orders": orders})
"""


# API for customer fetch orders
def get_restaurant_meals(request, restaurant_id):
    meals = MealSerializer(
        Meal.objects.filter(restaurant_id = restaurant_id).order_by("-id"),
        many=True,
        context={"request": request}
    ).data

    return JsonResponse({"meals": meals})


@csrf_exempt
# API for customer fetch reports
def get_restaurant_reports(request):
    if request.method == "POST":
        token = request.META['HTTP_AUTHORIZATION']
        user = Token.objects.get(key=token).user
        restaurant_id = user.restaurant.id

        # Calculate revenue and number of order by current week
        revenue = []
        orders = []

        # Calculate weekdays
        today = datetime.now()
        current_weekdays = [today + timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]

        for day in current_weekdays:
            delivered_orders = OrderSerializer(
                    Order.objects.filter(
                        restaurant=restaurant_id,
                        status=Order.DELIVERED,
                        created_at__year=day.year,
                        created_at__month=day.month,
                        created_at__day=day.day
                    ),
                    many=True,
                    context={"request": request}
                ).data
            revenue.append(sum(order['total'] for order in delivered_orders))
            orders.append(len(delivered_orders))

        # # Top 3 Drivers
        # top3_drivers = DriverSerializer(
        #         Driver.objects.annotate(
        #             total_order=Count(
        #                 Case(
        #                     When(order__restaurant=restaurant_id, then=1)
        #                 )
        #             )
        #         ).order_by("-total_order")[:3],
        #         many=True,
        #         context={"request": request}
        #     ).data
        #
        # driver = {
        #     "labels": [driver['name'] for driver in top3_drivers],
        #     "data": [driver['total_order'] for driver in top3_drivers]
        # }

        # Top 3 Meals
        top3_meals = MealSerializer(
            Meal.objects.filter(restaurant=restaurant_id)
                .annotate(total_order=Sum('orderdetail__quantity'))
                .order_by("-total_order")[:3],
            many=True,
            context={"request": request}
        ).data

        meal = {
            "labels": [meal['name'] for meal in top3_meals],
            "data": [meal['total_order'] or 0 for meal in top3_meals]
        }

        return JsonResponse({"payload": {"revenue": revenue, "orders": orders, "meal": meal},
                             "status": "true", "response": "Success"})


# API for customer add order
@csrf_exempt
def customer_add_order(request):
    """
        params:
            access_token
            restaurant_id
            address_line_1
            town
            order_detail (json format), example:
                [{"meal_id": 1, "quantity": 2},{"meal_id": 2, "quantity": 3}]
            stripe_token

        return:
            {"status": "success"}
    """

    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token=request.POST.get("access_token"), expires__gt=timezone.now())

        # Get profile
        customer = access_token.user.customer

        # Get Stripe token
        stripe_token = request.POST["stripe_token"]

        # Check whether customer has any order that is not delivered
        if Order.objects.filter(customer = customer).exclude(status = Order.DELIVERED):
            return JsonResponse({"status": "failed", "error": "Your last order must be completed."})

        # Check Address
        if not request.POST["address"]:
            return JsonResponse({"status": "failed", "error": "Address is required."})

        # Get Order Detail
        order_detail = json.loads(request.POST["order_detail"])

        order_total = 0
        for meal in order_detail:
            order_total += Meal.objects.get(id=meal["meal_id"]).price * meal["quantity"]

        if len(order_detail) > 0:

            # Step 1: Create a charge: this will charge customer's card
            charge = stripe.Charge.create(
                amount=order_total * 100, # Amount in ngn
                currency="ngn",
                source=stripe_token,
                description="Grabwack Order"
            )

            if charge.status != "failed":

                # Step 2 - Create an Order
                order = Order.objects.create(
                    customer=customer,
                    restaurant_id=request.POST["restaurant_id"],
                    total = order_total,
                    status = Order.COOKING,
                    address = request.POST["address"]
                )

                # Step 3 - Create Order details
                for meal in order_detail:
                    OrderDetail.objects.create(
                        order=order,
                        meal_id=meal["meal_id"],
                        quantity=meal["quantity"],
                        sub_total=Meal.objects.get(id=meal["meal_id"]).price * meal["quantity"]
                    )

                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "failed", "error": "Failed connect to Stripe."})


##############
# RESTAURANT NOTIFICATION
##############

def restaurant_order_notification(request, last_request_time):
    notification = Order.objects.filter(restaurant = request.user.restaurant,
        created_at__gt = last_request_time).count()

    return JsonResponse({"notification": notification})



# API for customer fetch latest order
def customer_latest_order(request):
    access_token = AccessToken.objects.get(token=request.GET.get("access_token"), expires__gt=timezone.now())

    customer = access_token.user.customer
    order = OrderSerializer(Order.objects.filter(customer = customer).last()).data

    return JsonResponse({"order": order})


##############
# DRIVERS
##############

def driver_get_ready_orders():
    orders = OrderSerializer(
        Order.objects.filter(status=Order.READY, driver=None).order_by("-id"),
        many=True
    ).data

    return JsonResponse({"orders": orders})


# API for driver registration
# POST
# params:
# Header: Authorization token
# Body: avatar, phone, address, location
@csrf_exempt
def driver_registration(request):
    if request.method == "POST":
        token = request.META['HTTP_AUTHORIZATION']
        user = Token.objects.get(key=token).user

        if len(request.FILES) != 0:
            f = request.FILES['avatar']
            file_path = os.path.join(os.getcwd(), 'media/driver_avatar/')
            fs = FileSystemStorage(location=file_path)
            filename = fs.save(f.name, f)
            image_url = 'driver_avatar/' + filename
        else:
            return JsonResponse({"payload": {}, "status": "false",
                                 "response": "Please select avatar."})

        form_data = {'name': user.id,
                     'phone': request.POST['phone'],
                     'address': request.POST['address'],
                     'location': request.POST['location'],
                     'avatar': image_url}
        query_dict = QueryDict('', mutable=True)
        query_dict.update(form_data)
        serializer = DriverRegistrationSerializer(data=query_dict)

        if serializer.is_valid():
            driver_data = DriverRegistrationSerializer(
                Driver.objects.filter(user_id=user.id),
                many=True,
                context={"request": request}
            ).data
            # Check if driver is already exists
            if len(driver_data) == 0:
                driver = serializer.save(
                    user_id=user.id
                )
                if driver:
                    saved_driver_data = DriverRegistrationSerializer(
                        Driver.objects.filter(user_id=user.id),
                        many=True,
                        context={"request": request}
                    ).data
                    return JsonResponse({"payload": {"driver": saved_driver_data[0]},
                                         "status": "true", "response": "Success"})
                else:
                    return JsonResponse({"payload": {}, "status": "false",
                                         "response": serializer.errors})
            else:
                return JsonResponse({"payload": {}, "status": "false",
                                     "response": "Already registered."})
        else:
            return JsonResponse({"payload": {}, "status": "false",
                                 "response": serializer.errors})


# Driver login
# POST
# params:
# Header: Authorization token
@csrf_exempt
def driver_login(request):
    if request.method == "POST":
        token = request.META['HTTP_AUTHORIZATION']
        user = Token.objects.get(key=token).user

        driver_data = DriverRegistrationSerializer(
            Driver.objects.filter(user_id=user.id),
            many=True,
            context={"request": request}
        ).data
        # Check if driver is already exists
        if len(driver_data) == 0:
            return JsonResponse({"payload": {}, "status": "false",
                                 "response": "You are not registered as driver.Please register"})
        else:
            return JsonResponse({"payload": {"driver": driver_data[0]},
                                 "status": "true", "response": "Success"})


@csrf_exempt
# POST
# params: access_token, order_id
def driver_pick_order(request):

    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token=request.POST.get("access_token"),expires__gt=timezone.now())

        # Get Driver
        driver = access_token.user.driver

        # Check if driver can only pick up one order at the same time
        if Order.objects.filter(driver=driver).exclude(status = Order.DELIVERED):
            return JsonResponse({"status": "failed", "error": "You can only pick one order at the same time."})

        try:
            order = Order.objects.get(
                id=request.POST["order_id"],
                driver=None,
                status=Order.READY
            )
            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()
            order.save()

            return JsonResponse({"status": "success"})

        except Order.DoesNotExist:
            return JsonResponse({"status": "failed", "error": "This order has been picked up by another."})

    return JsonResponse({})


# GET params: access_token
def driver_get_latest_order(request):
    # Get token
    access_token = AccessToken.objects.get(token=request.GET.get("access_token"), expires__gt=timezone.now())

    driver = access_token.user.driver
    order = OrderSerializer(
        Order.objects.filter(driver=driver).order_by("picked_at").last()
    ).data

    return JsonResponse({"order": order})


# POST params: access_token, order_id
@csrf_exempt
def driver_complete_order(request):
    # Get token
    access_token = AccessToken.objects.get(token=request.POST.get("access_token"), expires__gt=timezone.now())

    driver = access_token.user.driver

    order = Order.objects.get(id=request.POST["order_id"], driver=driver)
    order.status = Order.DELIVERED
    order.save()

    return JsonResponse({"status": "success"})


# GET params: access_token
def driver_get_revenue(request):
    access_token = AccessToken.objects.get(token=request.GET.get("access_token"), expires__gt=timezone.now())

    driver = access_token.user.driver

    from datetime import timedelta

    revenue = {}
    today = timezone.now()
    current_weekdays = [today + timedelta(days = i) for i in range(0 - today.weekday(), 7 - today.weekday())]

    for day in current_weekdays:
        orders = Order.objects.filter(
            driver=driver,
            status=Order.DELIVERED,
            created_at__year=day.year,
            created_at__month=day.month,
            created_at__day=day.day
        )

        revenue[day.strftime("%a")] = sum(order.total for order in orders)

    return JsonResponse({"revenue": revenue})


##############
# Driver and Customer location tracker
##############
# POST - params: access_token, "lat,lng"
@csrf_exempt
def driver_update_location(request):
    if request.method == "POST":
        access_token = AccessToken.objects.get(token=request.POST.get("access_token"), expires__gt=timezone.now())

        driver = access_token.user.driver

        # Set location string => database
        driver.location = request.POST["location"]
        driver.save()

        return JsonResponse({"status": "success"})


def customer_driver_location(request):
    access_token = AccessToken.objects.get(token=request.GET.get("access_token"), expires__gt=timezone.now())

    customer = access_token.user.customer

    # Get driver's location related to this customer's current order.
    current_order = Order.objects.filter(customer=customer, status=Order.DELIVERED).last()
    location = current_order.driver.location
    return JsonResponse({"location": location})
