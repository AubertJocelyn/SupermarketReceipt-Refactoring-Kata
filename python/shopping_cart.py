import math

from numba import typeof

import model_objects
from Offers.Bundle import Bundle
from Offers.SimpleDiscount import SimpleDiscount
from model_objects import ProductQuantity, Product


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
        for key in offers.keys():
            if isinstance(key, model_objects.Product):
                p = key
                if p in self._product_quantities.keys():
                    offer = offers[p]
                    if isinstance(offer, SimpleDiscount):
                        quantity = self._product_quantities[p]
                        unit_price = catalog.unit_price(p)
                        amount = offer.calculate_discount_amount(quantity, unit_price)
                        if amount < 0:
                            offer.set_discount_amount(amount)
                            receipt.add_discount(offer)
            elif all(isinstance(e, Product) for e in key):
                if all(p in self._product_quantities.keys() for p in key):
                    if isinstance(offers[key], Bundle):
                        quantities = [self._product_quantities[p] for p in key]
                        unit_prices = [catalog.unit_price(p) for p in key]
                        amount = offers[key].calculate_discount_amount(quantities, unit_prices)
                        if amount < 0:
                            offers[key].set_discount_amount(amount)
                            receipt.add_discount(offers[key])