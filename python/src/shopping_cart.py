import math

from model_objects import ProductQuantity, SpecialOfferType, Discount


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
                discount = self.get_discount(p, quantity=self._product_quantities[p], offer=offers[p], unit_price=catalog.unit_price(p))
                if discount:
                    receipt.add_discount(discount)

    def get_discount(self, p, quantity, offer, unit_price):
        if offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
            return self.get_discount_x_for_amount(p, quantity, unit_price, offer.argument, 2)

        elif offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
            return self.get_discount_x_for_amount(p, quantity, unit_price, offer.argument,5)

        elif offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
            return self.get_discount_x_for_amount(p, quantity, unit_price, 2 * unit_price,3)

        elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
            return self.get_discount_x_for_amount(p, quantity, unit_price, 0.9 * unit_price,1)
        else:
            return None

    def get_discount_x_for_amount(self, p, quantity, unit_price, amount, x):
        total = amount * (int(quantity) // x) + int(quantity) % x * unit_price
        discount_total = unit_price * quantity - total
        discount = Discount(p, str(x) + " for " + str(amount), -discount_total)
        return discount
