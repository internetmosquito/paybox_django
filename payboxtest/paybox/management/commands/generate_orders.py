import decimal
import random
from datetime import datetime
from paybox.models import Post
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates random orders, as many as specified'

    def add_arguments(self, parser):
        parser.add_argument('orders', type=int)

    def handle(self, *args, **options):
        import ipdb; ipdb.set_trace()
        n_orders = options['orders']
        john_smith, _ = User.objects.get_or_create(username='johnsmith')
        john_smith.email = 'john@smith.com'
        john_smith.save()
        # Remove all previus orders
        Post.objects.all().delete()

        for i in range(0, n_orders):
            order = Post()
            order.client = john_smith
            random_price = float(decimal.Decimal(random.randrange(15, 100)))
            order.total_incl_tax = random_price
            order.total_excl_tax = random_price
            # Use this field to indicate that an order is on hold / awaiting payment
            order.status = 'PENDING'
            order.save()
        self.stdout.write(self.style.SUCCESS('Successfully created orders!'))