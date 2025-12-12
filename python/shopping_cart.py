import math

from Offers.SimpleDiscount import SimpleDiscount
from model_objects import ProductQuantity


class ShoppingCart:

    def __init__(self):
        self._items = []
        self._product_quantities = {}

    @property
    def items(self):
        return self._items

    def add_item(self, product):
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] = self._product_quantities[product] + quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(self, receipt, offers, catalog):
        for p in self._product_quantities.keys():
            if p in offers.keys():
                offer = offers[p]
                if isinstance(offer, SimpleDiscount):
                    quantity = self._product_quantities[p]
                    unit_price = catalog.unit_price(p)
                    amount = offer.calculate_discount_amount(quantity, unit_price)
                    if amount < 0:
                        offer.set_discount_amount(amount)
                        receipt.add_discount(offer)
