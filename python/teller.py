from Client import Client
from OffersHandler import OffersHandler
from receipt import Receipt

class Teller:
    def __init__(self, catalog, client = None):
        self.catalog = catalog
        self.offers = {}
        if client:
            self.client = client
        else:
            self.client = Client()

    def add_special_offer(self, offer, product):
        self.offers[product] = offer

    def add_ticket_to_client(self, ticket):
        self.client.add_ticket(ticket)

    def add_fidelity_points_to_client(self, points):
        self.client.add_fidelity_points(points)

    def checks_out_articles_from(self, the_cart):
        the_cart.set_prices(self.catalog)
        receipt = Receipt()
        the_cart.add_products_to_recipe(receipt)
        receipt = OffersHandler(receipt, the_cart, self.offers, self.client.tickets).handle_offers()
        receipt.manage_fidelity_point(self.client)
        return receipt
