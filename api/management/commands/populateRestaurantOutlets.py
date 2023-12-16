from django.core.management.base import BaseCommand
from django.db.models import Count
import random
from datetime import datetime, timedelta
from faker import Faker
from api.models import *

fake = Faker()

'''
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
'''

class Command(BaseCommand):
    help = 'Command for Populating Users Table'

    def add_arguments(self, parser):
        parser.add_argument("outlet_limit", type=int, help='max outlet count for a restaurant')

    def handle(self, *args, **options):
        #get all the  users who have address < address limit and then populate their addresses
        outlet_limit = options['outlet_limit']
        #we do not get results in order by default since it's costly operation so here we really dont care so we will not be using order by
        restaurants_with_less_than_limit_outlets = Restaurant.objects.annotate(num_outlets=Count('restaurantoutlet')).filter(num_outlets__lt=outlet_limit)

        outlet_bulk = []
        ids = []
        #email would be unique almost but mobile no can be repeated.
        for restaurant in restaurants_with_less_than_limit_outlets:
            ids.append(restaurant.id)
            copies = outlet_limit - restaurant.num_outlets
            copies =  random.randint(0, copies)#random to select from limit
            for _ in range(copies):
                address={
                    "street": fake.street_address(),
                    "zipcode": fake.zipcode(),
                }
                name=fake.name()
                email = 'res'+str(restaurant.id)+'_'+name+'@foodverse.in'
                outlet = RestaurantOutlet(restaurant=restaurant, name=name, email=email, mobile=fake.phone_number(), address=address, is_verified=True, is_activated=True, city=fake.city())
                outlet_bulk.append(outlet)

        RestaurantOutlet.objects.bulk_create(outlet_bulk)

        self.stdout.write(self.style.SUCCESS('Successfully populated database.'))
        self.stdout.write(self.style.SUCCESS(ids))