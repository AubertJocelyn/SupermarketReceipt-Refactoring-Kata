from Discount import Discount
from model_objects import Product


class OffersHandler:
    def __init__(self, cart, receipt, offers):
        self.cart = cart
        self.receipt = receipt
        self.offers = offers
        self.valid_discounts = {}

    def handle_offers(self):
        self.set_valid_discounts()
        self.apply_discounts()
        return self.receipt

    def apply_discounts(self):
        for products in self.valid_discounts.keys():
            discount = self.valid_discounts[products]
            quantities = [self.cart.get_quantity(p) for p in products]
            unit_prices = [self.cart.get_price(p) for p in products]
            amount = discount.calculate_discount_amount(quantities, unit_prices)
            if amount < 0:
                discount.set_discount_amount(amount)
                self.receipt.add_discount(discount)

    def set_valid_discounts(self):
        for key in self.offers.keys():
            if all(isinstance(e, Product) for e in key):
                if all(p in self.cart.get_products() for p in key):
                    if isinstance(self.offers[key], Discount):
                        self.valid_discounts[key] = self.offers[key]