from django.core.management.base import BaseCommand
from django.db.models import Count
import random
from datetime import datetime, timedelta
from faker import Faker
from api.models import *

fake = Faker()

'''
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
'''

#email would be simply user_{userid}@foodverse.in #dummy emails
#for mobile start would be 1000000000 and we will increment it every time

class Command(BaseCommand):
    help = 'Command for Populating Users Table'

    def add_arguments(self, parser):
        parser.add_argument("address_limit", type=int, help='max address count for a user')

    def handle(self, *args, **options):
        #get all the  users who have address < address limit and then populate their addresses
        address_limit = options['address_limit']
        users_with_less_than_limit_addresses = User.objects.annotate(num_addresses=Count('useraddress')).filter(num_addresses__lt=address_limit)

        address_bulk = []

        for user in users_with_less_than_limit_addresses:
            copies = address_limit - user.num_addresses
            for _ in range(copies):
                address = UserAddress(user=user, name=fake.name(), line1=fake.street_address(), line2=fake.secondary_address(), pincode=fake.zipcode())
                address_bulk.append(address)

        UserAddress.objects.bulk_create(address_bulk)

        self.stdout.write(self.style.SUCCESS('Successfully populated database.'))

