from OffersHandler import OffersHandler
from receipt import Receipt


class Teller:

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}

    def add_special_offer(self, offer, product):
        self.offers[product] = offer

    def checks_out_articles_from(self, the_cart):
        the_cart.set_prices(self.catalog)
        receipt = Receipt()
        the_cart.add_products_to_receipt(receipt)
        receipt = OffersHandler(the_cart, receipt, self.offers).handle_offers()

        return receipt
