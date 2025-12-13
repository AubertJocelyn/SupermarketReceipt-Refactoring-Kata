import math

from numba import typeof

import model_objects
from Offers.Bundle import Bundle
from Offers.SimpleDiscount import SimpleDiscount
from Ticket import Ticket
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

    def handle_offers(self, receipt, offers, catalog, client_tickets):
        already_used_tickets = []
        for ticket in client_tickets:
            products = list(ticket.min_products_quantities.keys())
            quantities = [self._product_quantities[p] for p in products]
            if ticket.is_ticket_usable(products, quantities):
                offer = ticket.get_discount_offer()
                quantities = [ticket.max_products_quantities[p] for p in products]
                unit_prices = [catalog.unit_price(p) for p in products]
                amount = offer.calculate_discount_amount(quantities[0], unit_prices[0])
                if amount < 0:
                    already_used_tickets = [type(ticket)]
                    offer.set_discount_amount(amount)
                    receipt._ticket_discounts.append(offer)
                    client_tickets.remove(ticket)
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
                    if isinstance(offers[key], Ticket):
                        ticket = offers[key]
                        if not isinstance(ticket, tuple(already_used_tickets)):
                            products = key
                            quantities = [self._product_quantities[p] for p in products]
                            if ticket.is_ticket_triggered(products, quantities):
                                client_tickets.append(ticket)





