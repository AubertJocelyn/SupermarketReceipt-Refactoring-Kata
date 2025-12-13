from Offers.Bundle import Bundle
from Offers.SimpleDiscount import SimpleDiscount


class ReceiptItem:
    def __init__(self, product, quantity, price, total_price):
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = total_price


class Receipt:
    def __init__(self):
        self._items = []
        self._discounts = []
        self._ticket_discounts = []
        self.fidelity_points_gained = 0.0
        self.fidelity_points_used = 0.0
        self.fidelity_points_count = 0.0


    def total_price(self):
        total = 0
        for item in self.items:
            total += item.total_price
        for discount in self.discounts:
            if isinstance(discount, SimpleDiscount) or isinstance(discount, Bundle):
                total += discount.discount_amount
        for discount in self._ticket_discounts:
            total += discount.discount_amount
        total -= self.fidelity_points_used/100
        return total

    def add_product(self, product, quantity, price, total_price):
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount):
        self._discounts.append(discount)

    def add_ticket_discount(self, discount):
        self._ticket_discounts.append(discount)

    @property
    def items(self):
        return self._items[:]

    @property
    def discounts(self):
        return self._discounts[:]

    def manage_fidelity_point(self, client, fidelity_point_wish):
        self.fidelity_points_used = min(self.total_price(), min(max(0, fidelity_point_wish), client.fidelity_points))
        self.fidelity_points_gained = self.total_price() - self.fidelity_points_used
        self.fidelity_points_count = client.fidelity_points + self.fidelity_points_gained - self.fidelity_points_used
        client.fidelity_points = self.fidelity_points_count
