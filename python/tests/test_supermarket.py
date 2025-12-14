import unittest

from Discount import NForM, NForAmount, XPercentDiscount, UniformXPercentDiscountBundle
from Ticket import HalfPriceTicket
from model_objects import Product, ProductUnit
from receipt_printer import ReceiptPrinter
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


class SupermarketTest(unittest.TestCase):
    def get_catalog_test(self):
        catalog = FakeCatalog()
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        catalog.add_product(toothbrush, 0.99)

        apples = Product("apples", ProductUnit.KILO)
        catalog.add_product(apples, 1.99)
        return catalog

    def get_catal_tel_cart_test(self, quantity_toothbrush):
        catalog = self.get_catalog_test()
        teller = Teller(catalog)
        cart = ShoppingCart()
        cart.add_item_quantity(catalog.products["apples"], 2.5)
        if quantity_toothbrush:
            cart.add_item_quantity(catalog.products["toothbrush"], quantity_toothbrush)
        return catalog, teller, cart

    def test_generic(self):
        catalog, teller, cart = self.get_catal_tel_cart_test(None)

        receipt = teller.checks_out_articles_from(cart)
        print(ReceiptPrinter().print_receipt(receipt))

        self.assert_price_and_len_receipt(receipt, 4.975, 0, 1)
        receipt_item = receipt.items[0]
        self.assertEqual(catalog.products["apples"], receipt_item.product)
        self.assertEqual(1.99, receipt_item.price)
        self.assertAlmostEqual(receipt_item.total_price, 2.5 * 1.99, places=2)
        self.assertEqual(2.5, receipt_item.quantity)

    def test_ten_percent_discount(self):
        catalog, teller, cart = self.get_catal_tel_cart_test(1.0)

        discount = XPercentDiscount(catalog.products["toothbrush"], 10.0)
        teller.add_special_offer(discount, (catalog.products["toothbrush"],))
        receipt = teller.checks_out_articles_from(cart)
        self.assert_price_and_len_receipt(receipt, 5.866, 1, 2)

    def test_three_for_two_discount(self):
        catalog, teller, cart = self.get_catal_tel_cart_test(3.0)

        discount = NForM(catalog.products["toothbrush"], 3, 2)
        teller.add_special_offer(discount, (catalog.products["toothbrush"],))
        receipt = teller.checks_out_articles_from(cart)
        self.assert_price_and_len_receipt(receipt, 6.955, 1, 2)


    def test_three_for_two_discount_bis(self):
        catalog, teller, cart = self.get_catal_tel_cart_test(2.0)

        discount = NForM(catalog.products["toothbrush"], 3, 2)
        teller.add_special_offer(discount, (catalog.products["toothbrush"],))
        receipt = teller.checks_out_articles_from(cart)
        self.assert_price_and_len_receipt(receipt, 6.955, 0, 2)

    def test_five_for_amount(self):
        catalog, teller, cart = self.get_catal_tel_cart_test(7.0)

        discount = NForAmount(catalog.products["toothbrush"], 5, 4.0)
        teller.add_special_offer(discount, (catalog.products["toothbrush"],))
        receipt = teller.checks_out_articles_from(cart)
        self.assert_price_and_len_receipt(receipt, 10.955, 1, 2)

    def test_two_for_amount(self):
        catalog, teller, cart = self.get_catal_tel_cart_test(2.0)

        breaker = Product("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", ProductUnit.EACH)
        catalog.add_product(breaker, 0.99)

        cart.add_item_quantity(catalog.products["abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"], 0.0)
        discount = NForAmount((catalog.products["toothbrush"],), 2, 1.90)
        teller.add_special_offer(discount, (catalog.products["toothbrush"],))

        receipt = teller.checks_out_articles_from(cart)
        print("\n")
        print(ReceiptPrinter().print_receipt(receipt))
        self.assert_price_and_len_receipt(receipt, 6.875, 1, 3)

    def test_bundle(self):
        catalog, teller, cart = self.get_catal_tel_cart_test(1.0)

        toothpaste = Product("toothpaste", ProductUnit.EACH)
        catalog.add_product(toothpaste, 1.79)

        cart.add_item_quantity(toothpaste, 1.0)

        bundle = UniformXPercentDiscountBundle((catalog.products["toothpaste"], catalog.products["toothbrush"]), 10.0)
        teller.add_special_offer(bundle, (catalog.products["toothpaste"], catalog.products["toothbrush"]))

        receipt = teller.checks_out_articles_from(cart)
        print("\n")
        print(ReceiptPrinter().print_receipt(receipt))
        self.assert_price_and_len_receipt(receipt, 7.477, 1, 3)

    def assert_price_and_len_receipt(self, receipt, price, a, b):
        self.assertEqual(a, len(receipt.discounts))
        self.assertEqual(b, len(receipt.items))
        self.assertAlmostEqual(receipt.total_price(), price, places=2)

    def test_use_ticket(self):
        catalog, teller, cart = self.get_catal_tel_cart_test(6.0)

        min_products_quantities = {catalog.products["toothbrush"]: 6}
        max_products_quantities = {catalog.products["toothbrush"]: 6}
        discounted_products_quantities = {catalog.products["toothbrush"]: 6}

        ticket = HalfPriceTicket(1765613954,	1766560800, min_products_quantities, max_products_quantities, discounted_products_quantities)
        teller.add_special_offer(ticket, (catalog.products["toothbrush"],))

        teller.add_ticket_to_client(ticket)

        receipt = teller.checks_out_articles_from(cart)

        print(ReceiptPrinter().print_receipt(receipt))

        self.assertEqual(0, len(teller.client.tickets))
        self.assertEqual(1, len(receipt._ticket_discounts))

    def test_gain_ticket(self):
        catalog, teller, cart = self.get_catal_tel_cart_test(6.0)

        min_products_quantities = {catalog.products["toothbrush"]: 6}
        max_products_quantities = {catalog.products["toothbrush"]: 6}
        discounted_products_quantities = {catalog.products["toothbrush"]: 6}

        ticket = HalfPriceTicket(1765613954, 1766560800, min_products_quantities, max_products_quantities,
                                 discounted_products_quantities)
        teller.add_special_offer(ticket, (catalog.products["toothbrush"],))

        receipt = teller.checks_out_articles_from(cart)

        self.assertEqual(1, len(teller.client.tickets))
        self.assertEqual(0, len(receipt._ticket_discounts))


