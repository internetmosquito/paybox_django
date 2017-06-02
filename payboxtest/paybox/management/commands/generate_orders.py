import decimal
import random
from datetime import datetime
from paybox.models import Post
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    A simple Command to generate orders with random total amount but same client,
    will delete previous PAID ones, since PayBox will not accept a transaction with
    a used order reference
    Usage:
        python manage.py generate_order <num_orders>
    """
    help = 'Creates random orders, as many as specified'

    def add_arguments(self, parser):
        parser.add_argument('orders', type=int)

    def handle(self, *args, **options):
        n_orders = options['orders']
        john_smith, _ = User.objects.get_or_create(username='johnsmith')
        john_smith.email = 'john@smith.com'
        john_smith.save()
        # Remove all previus orders
        Post.objects.filter(status__in='PAID').delete()

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