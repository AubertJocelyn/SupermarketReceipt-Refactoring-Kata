from abc import abstractmethod

from Offers.Offer import Offer

class Bundle(Offer):
    def __init__(self, products):
        self.products = products

    def set_discount_amount(self, amount):
        self.discount_amount = amount

    @abstractmethod
    def get_message(self):
        pass

    @abstractmethod
    def calculate_discount_amount(self, quantities, unit_prices):
        pass

class UniformXPercentDiscountBundle(Bundle):
    def __init__(self, products, x):
        super().__init__(products)
        self.x = x

    def get_message(self):
        return [f"{self.x}% of" for i in range(len(self.products))]

    def calculate_discount_amount(self, quantities, unit_prices):
        base_price = 0
        discounted_price = 0
        for i in range(len(quantities)):
            base_price += quantities[i] * unit_prices[i]
            discounted_price += (1 - self.x/100.0) * int(quantities[i]) * unit_prices[i]
        return discounted_price - base_price