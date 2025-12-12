from abc import abstractmethod
from Offers.Offer import Offer


class SimpleDiscount(Offer):
    discount_amount: float
    def __init__(self, product):
        self.product = product

    def set_discount_amount(self, amount):
        self.discount_amount = amount

    @abstractmethod
    def get_message(self):
        pass

    @abstractmethod
    def calculate_discount_amount(self, quantity, unit_price):
        pass

class NForAmount(SimpleDiscount):
    def __init__(self, product, N, amount):
        super().__init__(product)
        self.N = N
        self.amount = amount

    def get_message(self):
        return f"{self.N} for {self.amount}"

    def calculate_discount_amount(self, quantity, unit_price):
        base_price = quantity * unit_price
        discounted_price = self.amount * (int(quantity) // self.N) + int(quantity) % self.N * unit_price
        return discounted_price - base_price

class NForM(SimpleDiscount):
    def __init__(self, product, N, M):
        super().__init__(product)
        self.N = N
        self.M = M

    def get_message(self):
        return f"{self.N} for {self.M}"

    def calculate_discount_amount(self, quantity, unit_price):
        base_price = quantity * unit_price
        discounted_price = self.M * unit_price * (int(quantity) // self.N) + int(quantity) % self.N * unit_price
        return discounted_price - base_price

class XPercentDiscount(SimpleDiscount):
    def __init__(self, product, x):
        super().__init__(product)
        self.x = x

    def get_message(self):
        return f"{self.x}% of"

    def calculate_discount_amount(self, quantity, unit_price):
        base_price = quantity * unit_price
        discounted_price = (1 - self.x/100.0) * unit_price * int(quantity)
        return discounted_price - base_price