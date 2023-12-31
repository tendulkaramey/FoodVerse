from django.core.management.base import BaseCommand
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
        parser.add_argument("count", type=int, help='rows you want to populate')

    def handle(self, *args, **options):
        #users will be appended with already users
        #get last user
        count = options['count']
        user = User.objects.all().order_by('-id')
        if user.count():
            last_user = user[0]
            mobile_no = int(last_user.mobile)
            new_id = last_user.id + 1
        else:
            #start populating from start
            mobile_no = 1000000000
            new_id = 1
        user_bulk = []
        for i in range(0, count):
            if mobile_no >= 9999999999:
                self.stdout.write(self.style.SUCCESS('Mobile Number Limit Reached'))
                break
            mobile_no = mobile_no + 1
            email = 'user_'+str(new_id)+'@foodverse.in'
            new_id += 1
            user_temp = User(first_name=fake.first_name(), last_name=fake.last_name(), email=email, mobile=mobile_no, is_verified=True, is_activated=True)
            user_bulk.append(user_temp)

        User.objects.bulk_create(user_bulk)

        self.stdout.write(self.style.SUCCESS('Successfully populated database.'))

