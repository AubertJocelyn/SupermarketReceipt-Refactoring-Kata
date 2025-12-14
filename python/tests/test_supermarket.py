import unittest

from model_objects import Product, SpecialOfferType, ProductUnit
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

    def get_catal_tel_cart_test(self, quantity_toothbrush, offer_type, argument):
        catalog = self.get_catalog_test()
        teller = Teller(catalog)
        cart = ShoppingCart()
        cart.add_item_quantity(catalog.products["apples"], 2.5)
        if quantity_toothbrush:
            cart.add_item_quantity(catalog.products["toothbrush"], quantity_toothbrush)
        teller.add_special_offer(offer_type, (catalog.products["toothbrush"]), argument)
        return catalog, teller, cart

    def test_generic(self):
        catalog, teller, cart = self.get_catal_tel_cart_test(None, SpecialOfferType.TEN_PERCENT_DISCOUNT, 10.0)

        receipt = teller.checks_out_articles_from(cart)
        print(ReceiptPrinter().print_receipt(receipt))

        self.assert_price_and_len_receipt(receipt, 4.975, 0, 1)
        receipt_item = receipt.items[0]
        self.assertEqual(catalog.products["apples"], receipt_item.product)
        self.assertEqual(1.99, receipt_item.price)
        self.assertAlmostEqual(receipt_item.total_price, 2.5 * 1.99, places=2)
        self.assertEqual(2.5, receipt_item.quantity)

    def simple_test(self, quantity_toothbrush, offer_type, argument, total_price, a, b):
        catalog, teller, cart = self.get_catal_tel_cart_test(quantity_toothbrush, offer_type, argument)
        receipt = teller.checks_out_articles_from(cart)
        self.assert_price_and_len_receipt(receipt, total_price, a, b)

    def test_ten_percent_discount(self):
        self.simple_test(1.0, SpecialOfferType.TEN_PERCENT_DISCOUNT, 10.0, 5.866, 1, 2)

    def test_three_for_two_discount(self):
        self.simple_test(3.0, SpecialOfferType.THREE_FOR_TWO, None, 6.955, 1, 2)

    def test_three_for_two_discount_bis(self):
        self.simple_test(2.0, SpecialOfferType.THREE_FOR_TWO, None, 6.955, 0, 2)

    def test_five_for_amount(self):
        self.simple_test(7.0, SpecialOfferType.FIVE_FOR_AMOUNT, 4.0, 10.955, 1, 2)

    def test_two_for_amount(self):
        catalog, teller, cart = self.get_catal_tel_cart_test(2.0, SpecialOfferType.TWO_FOR_AMOUNT, 1.90)

        breaker = Product("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", ProductUnit.EACH)
        catalog.add_product(breaker, 0.99)

        cart.add_item_quantity(catalog.products["abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"], 0.0)
        receipt = teller.checks_out_articles_from(cart)
        print("\n")
        print(ReceiptPrinter().print_receipt(receipt))
        self.assert_price_and_len_receipt(receipt, 6.875, 1, 3)

    def assert_price_and_len_receipt(self, receipt, price, a, b):
        self.assertEqual(a, len(receipt.discounts))
        self.assertEqual(b, len(receipt.items))
        self.assertAlmostEqual(receipt.total_price(), price, places=2)


