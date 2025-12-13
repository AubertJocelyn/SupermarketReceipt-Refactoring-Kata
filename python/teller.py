from Client import Client
from receipt import Receipt

class Teller:
    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}
        self.client_tickets = []

    def add_special_offer(self, offer, product):
        self.offers[product] = offer

    def add_ticket(self, ticket):
        self.client_tickets.append(ticket)

    def checks_out_articles_from(self, the_cart, client = None):
        if not client:
            client = Client()
        receipt = Receipt()
        product_quantities = the_cart.items
        for pq in product_quantities:
            p = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.unit_price(p)
            price = quantity * unit_price
            receipt.add_product(p, quantity, unit_price, price)

        the_cart.handle_offers(receipt, self.offers, self.catalog, self.client_tickets)

        receipt.manage_fidelity_point(client, 0.0)

        return receipt
