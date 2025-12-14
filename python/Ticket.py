from abc import abstractmethod
from typing import Dict

from Offers.Discount import NForM
from model_objects import Product


class Ticket:
    start_valididy: float
    end_validity: float
    min_products_quantities: Dict[Product, float]
    max_products_quantities: Dict[Product, float]
    triggering_products_quantities: Dict[Product, float]
    def __init__(self, start_valididy, end_validity, min_products_quantities, max_products_quantities, discounted_products_quantities):
        self.start_valididy = start_valididy
        self.end_validity = end_validity
        self.min_products_quantities = min_products_quantities
        self.max_products_quantities = max_products_quantities
        self.triggering_products_quantities = discounted_products_quantities

    def is_ticket_triggered(self, products, quantities):
        return all(products[i] in self.triggering_products_quantities.keys()\
               and quantities[i] >= self.triggering_products_quantities[products[i]]\
               for i in range(len(products)))

    def is_ticket_usable(self, products, quantities):
        b1 = self.start_valididy< self.current_date() < self.end_validity
        b2 = all(products[i] in self.min_products_quantities.keys() \
                   and quantities[i] >= self.min_products_quantities[products[i]] \
                   for i in range(len(products)))
        return b1 and b2

    def current_date(self):
        return (self.start_valididy + self.end_validity) / 2

    @abstractmethod
    def get_discount_offer(self):
        pass

class HalfPriceTicket(Ticket):
    def __init__(self, start_valididy, end_validity, min_products_quantities, max_products_quantities, discounted_products_quantities):
        super().__init__(start_valididy, end_validity, min_products_quantities, max_products_quantities, discounted_products_quantities)

    def get_discount_offer(self):
        return NForM(list(self.min_products_quantities.keys()), 1.0, 0.5)





