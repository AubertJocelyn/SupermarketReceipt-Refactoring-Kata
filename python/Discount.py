from abc import abstractmethod


class Discount():
    discount_amount: float
    def __init__(self, product):
        self.products = product

    def set_discount_amount(self, amount): self.discount_amount = amount

    @abstractmethod
    def get_message(self): pass

    @abstractmethod
    def calculate_discount_amount(self, quantities, unit_prices): pass

class NForAmountSchemeDiscount(Discount):
    def __init__(self, product):
        super().__init__(product)

    def getNForAmount(self, N, amount, quantity, unit_price):
        base_price = quantity * unit_price
        discounted_price = amount * (int(quantity) // N) + int(quantity) % N * unit_price
        return discounted_price - base_price



class NForAmount(NForAmountSchemeDiscount):
    def __init__(self, product, N, amount):
        super().__init__(product)
        self.N = N
        self.amount = amount

    def get_message(self): return f"{self.N} for {self.amount}"

    def calculate_discount_amount(self, quantities, unit_prices):
        return self.getNForAmount(self.N, self.amount, quantities, unit_prices)



class NForM(NForAmountSchemeDiscount):
    def __init__(self, product, N, M):
        super().__init__(product)
        self.N = N
        self.M = M

    def get_message(self): return f"{self.N} for {self.M}"

    def calculate_discount_amount(self, quantities, unit_prices):
        return self.getNForAmount(self.N, self.M * unit_prices, quantities, unit_prices)



class XPercentDiscount(NForAmountSchemeDiscount):
    def __init__(self, product, x):
        super().__init__(product)
        self.x = x

    def get_message(self): return f"{self.x}% of"

    def calculate_discount_amount(self, quantities, unit_prices):
        return self.getNForAmount(1.0, (1 - self.x/100) * unit_prices, quantities, unit_prices)