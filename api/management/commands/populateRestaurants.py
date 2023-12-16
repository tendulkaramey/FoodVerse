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
    help = 'Command for Populating Restaurant Table'

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help='max address count for restaurant')

    def handle(self, *args, **options):
        #get all the  users who have address < address limit and then populate their addresses

        count = options['count']

        restaurant_bulk = []

        for _ in range(count):
            restaurant = Restaurant(name=fake.company(), is_activated=True, is_verified=True)
            restaurant_bulk.append(restaurant)


        Restaurant.objects.bulk_create(restaurant_bulk)

        self.stdout.write(self.style.SUCCESS('Successfully populated database.'))

