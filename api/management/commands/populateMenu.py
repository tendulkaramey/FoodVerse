from django.core.management.base import BaseCommand
from django.db.models import Count
import random
from datetime import datetime, timedelta
from faker import Faker
from api.models import *

fake = Faker()

'''
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
'''

#will create proper menu with orignial names later, now just using faker to populate this bcs purpose is to learn about db at scale.

class Command(BaseCommand):
    help = 'Command for Populating Menu Table'

    def add_arguments(self, parser):
        parser.add_argument("menu_limit", type=int, help='max menu item count for a restaurant outlet')

    def handle(self, *args, **options):
        menu_limit = options['menu_limit']
        #we do not get results in order by default since it's costly operation so here we really dont care so we will not be using order by
        outlets_with_less_than_limit_menu = RestaurantOutlet.objects.annotate(num_menu=Count('menu')).filter(num_menu__lt=menu_limit)

        menu_bulk = []
        ids = []
        #email would be unique almost but mobile no can be repeated.
        for outlet in outlets_with_less_than_limit_menu:
            ids.append(outlet.id)
            copies = menu_limit - outlet.num_menu
            copies =  random.randint(0, copies)#random to select from limit
            for _ in range(copies):
                price = '{:.2f}'.format(random.uniform(20, 1000))
                item = Menu(outlet=outlet, name=fake.word(), price=price, description=fake.text(max_nb_chars=500), image_url=fake.image_url(), food_type=random.choice(['Veg', 'Non-Veg']), is_avaliable=fake.boolean(chance_of_getting_true=70), rating=random.uniform(0, 5), additional_data={})
                menu_bulk.append(item)

        Menu.objects.bulk_create(menu_bulk)

        self.stdout.write(self.style.SUCCESS('Successfully populated database.'))
        self.stdout.write(self.style.SUCCESS(ids))