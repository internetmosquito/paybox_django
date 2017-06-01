from __future__ import unicode_literals
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):
    client = models.ForeignKey('auth.User')

    reference = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    # Billing address is not always required (eg paying by gift card)
    billing_address = models.CharField(_("BillingAddress"), max_length=50, blank=True)

    currency = models.CharField(_("Currency"), max_length=12, default='Euro')

    total_incl_tax = models.DecimalField(_("Order total (inc. tax)"), decimal_places=2, max_digits=12)
    total_excl_tax = models.DecimalField(_("Order total (excl. tax)"), decimal_places=2, max_digits=12)

    # Shipping charges
    shipping_incl_tax = models.DecimalField(_("Shipping charge (inc. tax)"), decimal_places=2, max_digits=12, default=0)
    shipping_excl_tax = models.DecimalField(_("Shipping charge (excl. tax)"), decimal_places=2, max_digits=12, default=0)

    # Use this field to indicate that an order is on hold / awaiting payment
    status = models.CharField(_("Status"), max_length=100, blank=True)

    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.reference)