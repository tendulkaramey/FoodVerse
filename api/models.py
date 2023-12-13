from django.db import models
from django.utils.timezone import now

def default_json():
    return {}

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now, editable=False)

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    line1 = models.CharField(max_length=100)
    line2 = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=now, editable=False)

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now, editable=False)

class RestaurantOutlet(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    city = models.CharField(max_length=50)
    address = models.JSONField(default=default_json)
    mobile = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=now, editable=False)

class Menu(models.Model):
    outlet = models.ForeignKey(RestaurantOutlet, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    description = models.CharField(max_length=500)
    image_url = models.CharField(max_length=250)
    food_type = models.CharField(max_length=10)
    is_avaliable = models.BooleanField(default=False)
    additional_data = models.JSONField(default=default_json)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=False)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    outlet = models.ForeignKey(RestaurantOutlet, on_delete=models.CASCADE)
    user_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    total = models.FloatField(blank=False)
    items = models.JSONField(default=default_json)
    created_at = models.DateTimeField(default=now, editable=False)

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(blank=False)
    created_at = models.DateTimeField(default=now, editable=False)

class ItemReview(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    comment = models.CharField(max_length=150)
    rating = models.FloatField(default=5)
    created_at = models.DateTimeField(default=now, editable=False)