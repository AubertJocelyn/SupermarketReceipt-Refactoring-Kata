from Discount import Discount
from Ticket import Ticket
from model_objects import Product


class OffersHandler:
    def __init__(self, receipt, cart, offers, client_tickets):
        self.cart = cart
        self.receipt = receipt
        self.offers = offers
        self.client_tickets = client_tickets
        self.already_used_tickets = []
        self.valid_discounts = {}
        self.valid_tickets = {}

    def handle_offers(self):
        self.spend_tickets()
        self.set_valid_tickets()
        self.gain_tickets()
        self.set_valid_discounts()
        self.apply_discounts()
        return self.receipt

    def spend_tickets(self):
        for ticket in self.client_tickets:
            products = list(ticket.min_products_quantities.keys())
            quantities = [self.cart.get_quantity(p) for p in products]
            if ticket.is_ticket_usable(products, quantities):
                quantities = [ticket.max_products_quantities[p] for p in products]
                unit_prices = [self.cart.get_price(p) for p in products]
                self.apply_ticket_discount(ticket, quantities, unit_prices)

    def apply_ticket_discount(self, ticket, quantities, unit_prices):
        offer = ticket.get_discount_offer()
        amount = offer.calculate_discount_amount(quantities, unit_prices)
        if amount < 0:
            self.already_used_tickets = [type(ticket)]
            offer.set_discount_amount(amount)
            self.receipt._ticket_discounts.append(offer)
            self.client_tickets.remove(ticket)

    def gain_tickets(self):
        for products in self.valid_tickets.keys():
            ticket = self.offers[products]
            quantities = [self.cart.get_quantity(p) for p in products]
            if ticket.is_ticket_obtain(products, quantities):
                self.client_tickets.append(ticket)

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

    def set_valid_tickets(self):
        for key in self.offers.keys():
            if all(isinstance(e, Product) for e in key):
                if all(p in self.cart.get_products() for p in key):
                    if isinstance(self.offers[key], Ticket):
                        if not isinstance(self.offers[key], tuple(self.already_used_tickets)):
                            self.valid_tickets[key] = self.offers[key]