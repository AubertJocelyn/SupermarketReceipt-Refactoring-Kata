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

def bundlise_calculate_amount_discount(fun):
    def wrapper(self, quantities, unit_prices):
        return fun(self, quantities[0], unit_prices[0])
    return wrapper

def bundlise_get_message(fun):
    def wrapper(self):
        return [fun(self)]
    return wrapper

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

    @bundlise_get_message
    def get_message(self): return f"{self.N} for {self.amount}"

    @bundlise_calculate_amount_discount
    def calculate_discount_amount(self, quantities, unit_prices):
        return self.getNForAmount(self.N, self.amount, quantities, unit_prices)



class NForM(NForAmountSchemeDiscount):
    def __init__(self, product, N, M):
        super().__init__(product)
        self.N = N
        self.M = M

    @bundlise_get_message
    def get_message(self): return f"{self.N} for {self.M}"

    @bundlise_calculate_amount_discount
    def calculate_discount_amount(self, quantities, unit_prices):
        return self.getNForAmount(self.N, self.M * unit_prices, quantities, unit_prices)



class XPercentDiscount(NForAmountSchemeDiscount):
    def __init__(self, product, x):
        super().__init__(product)
        self.x = x

    @bundlise_get_message
    def get_message(self): return f"{self.x}% of"

    @bundlise_calculate_amount_discount
    def calculate_discount_amount(self, quantities, unit_prices):
        return self.getNForAmount(1.0, (1 - self.x/100) * unit_prices, quantities, unit_prices)