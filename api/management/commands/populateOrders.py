from django.core.management.base import BaseCommand
from django.db.models import Count
import random
from datetime import datetime, timedelta
from faker import Faker
from api.models import *

fake = Faker()

'''
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
'''


class Command(BaseCommand):
    help = 'Command for Populating Menu Table'

    def add_arguments(self, parser):
        parser.add_argument("order_limit", type=int, help='orders to populate')

    def handle(self, *args, **options):
        order_limit = options['order_limit']

        users = User.objects.filter(is_activated=True)
        outlets = RestaurantOutlet.objects.filter(is_activated=True)

        for _ in range(order_limit):
            user = random.choice(users)
            outlet = random.choice(outlets)
            menus = Menu.objects.filter(outlet=outlet, is_avaliable=True)
            item_count = random.randint(1, 10)
            if menus.count() < item_count:
                order_items = list(menus)
            else:
                order_items = random.sample(list(menus), item_count)
            
            total = 0

            #select address of user for now take 1st address
            address = user.useraddress_set.all()[0]
            item_list_json = []
            qtys = []
            prices = []
            for item in order_items:
                item_data = {}
                qty = random.randint(1, 5)
                total += item.price * qty
                item_data['id'] = item.id
                item_data['quantity'] = qty
                item_data['price'] = item.price
                item_list_json.append(item_data)
                qtys.append(qty)
                prices.append(item.price)
            total = '{:.2f}'.format(total)
            order = Order(user=user, outlet=outlet, user_address=address, total=total, items=item_list_json)
            order.save()
            order_bulk = []
            for i in range(0, len(order_items)):
                order_item = OrderItems(order=order, item=order_items[i], quantity=qtys[i], price=prices[i])
                order_bulk.append(order_item)

            OrderItems.objects.bulk_create(order_bulk)
                


        self.stdout.write(self.style.SUCCESS('Successfully populated database.'))