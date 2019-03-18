# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
# from shop.modifiers.pool import cart_modifiers_pool
# from shop.serializers.cart import ExtraCartRow
from shop.modifiers.base import ShippingModifier, PaymentModifier
# from shop.money import Money
from shop.payment.defaults import CashOnDeliveryPayment
from shop.shipping.defaults import DefaultShippingProvider
# from djng.forms import fields
# from shop_stripe import modifiers


class PostalShippingModifier(ShippingModifier):
    identifier = 'postal-shipping'

    def __str__(self):
        return _("Postal shipping (Ukrposhta)")

    def get_choice(self):
        return self.identifier, _("Postal shipping (Ukrposhta)")

    # def add_extra_cart_row(self, cart, request):
    #     if not self.is_active(cart) and len(cart_modifiers_pool.get_shipping_modifiers()) > 1:
    #         return
    #     # add a shipping flat fee
    #     amount = Money('5')
    #     instance = {'label': _("Shipping costs"), 'amount': amount}
    #     cart.extra_rows[self.identifier] = ExtraCartRow(instance)
    #     cart.total += amount


class AddressDeliveryModifier(ShippingModifier):
    identifier = 'address-delivery'

    def get_choice(self):
        return self.identifier, _("Address delivery")


class CustomerPickupModifier(ShippingModifier):
    identifier = 'customer-pickup'
    extra_fields = {}

    def get_choice(self):
        return self.identifier, _("Customer pickups the goods")

    def get_extra_field(self):
        return self.extra_fields


class NovaPoshtaModifier(ShippingModifier):
    identifier = 'nova-poshta-shipping'
    shipping_provider = DefaultShippingProvider()

    def get_choice(self):
        return self.identifier, _('Shipping with "Nova Poshta"')

#
# class StripePaymentModifier(modifiers.StripePaymentModifier):
#     commision_percentage = 3


class CashOnDeliveryPaymentModifier(PaymentModifier):
    identifier = 'cash-on-delivery-payment'
    payment_provider = CashOnDeliveryPayment()

    def get_choice(self):
        return self.identifier, _("Cash on delivery")
