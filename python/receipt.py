from Discount import Discount


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
            if isinstance(discount, Discount):
                total += discount.discount_amount
        for discount in self._ticket_discounts:
            total += discount.discount_amount
        return total

    def add_product(self, product, quantity, price, total_price):
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount):
        self._discounts.append(discount)

    @property
    def items(self):
        return self._items[:]

    @property
    def discounts(self):
        return self._discounts[:]
