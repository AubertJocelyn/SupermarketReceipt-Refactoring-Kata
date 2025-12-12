import unittest

from Offers.SimpleDiscount import NForAmount, NForM, XPercentDiscount
from model_objects import Product, SpecialOfferType, ProductUnit
from receipt_printer import ReceiptPrinter
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


class SupermarketTest(unittest.TestCase):
    def get_test_catalog(self):
        catalog = FakeCatalog()
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        catalog.add_product(toothbrush, 0.99)

        apples = Product("apples", ProductUnit.KILO)
        catalog.add_product(apples, 1.99)

        return catalog

    def get_test_discount_cart(self):
        return

    def test_generic(self):
        catalog = self.get_test_catalog()

        teller = Teller(catalog)

        cart = ShoppingCart()
        cart.add_item_quantity(catalog.products["apples"], 2.5)

        discount = XPercentDiscount(catalog.products["toothbrush"], 10.0)
        teller.add_special_offer(discount, catalog.products["toothbrush"])

        receipt = teller.checks_out_articles_from(cart)

        #Fake Catalog entièrement testé avant cette ligne
        self.assertAlmostEqual(receipt.total_price(), 4.975, places=2)
        self.assertEqual([], receipt.discounts)
        self.assertEqual(1, len(receipt.items))
        receipt_item = receipt.items[0]
        self.assertEqual(catalog.products["apples"], receipt_item.product)
        self.assertEqual(1.99, receipt_item.price)
        self.assertAlmostEqual(receipt_item.total_price, 2.5 * 1.99, places=2)
        self.assertEqual(2.5, receipt_item.quantity)

    #testsA
    def test_ten_percent_discount(self):
        catalog, teller, cart = self.get_catalog_teller_and_cart_test_A(1.0)

        discount = XPercentDiscount(catalog.products["toothbrush"], 10.0)
        teller.add_special_offer(discount, catalog.products["toothbrush"])
        receipt = teller.checks_out_articles_from(cart)
        self.assertAlmostEqual(receipt.total_price(), 5.866, places=2)
        self.assertEqual(1, len(receipt.discounts))
        self.assertEqual(2, len(receipt.items))

    def test_three_for_two_discount(self):
        catalog, teller, cart = self.get_catalog_teller_and_cart_test_A(3.0)

        discount = NForM(catalog.products["toothbrush"], 3, 2)
        teller.add_special_offer(discount, catalog.products["toothbrush"])
        receipt = teller.checks_out_articles_from(cart)
        self.assertAlmostEqual(receipt.total_price(), 6.955, places=2)
        self.assertEqual(1, len(receipt.discounts))
        self.assertEqual(2, len(receipt.items))


    def test_three_for_two_discount_bis(self):
        catalog, teller, cart = self.get_catalog_teller_and_cart_test_A(2.0)

        discount = NForM(catalog.products["toothbrush"], 3, 2)
        teller.add_special_offer(discount, catalog.products["toothbrush"])
        receipt = teller.checks_out_articles_from(cart)
        self.assertAlmostEqual(receipt.total_price(), 6.955, places=2)
        self.assertEqual(0, len(receipt.discounts))
        self.assertEqual(2, len(receipt.items))


    def test_five_for_amount(self):
        catalog, teller, cart = self.get_catalog_teller_and_cart_test_A(7.0)

        discount = NForAmount(catalog.products["toothbrush"], 5, 4.0)
        teller.add_special_offer(discount, catalog.products["toothbrush"])
        receipt = teller.checks_out_articles_from(cart)
        self.assertAlmostEqual(receipt.total_price(), 10.955, places=2)
        self.assertEqual(1, len(receipt.discounts))
        self.assertEqual(2, len(receipt.items))

    def test_two_for_amount(self):
        catalog, teller, cart = self.get_catalog_teller_and_cart_test_A(2.0)

        discount = NForAmount(catalog.products["toothbrush"], 2, 1.90)
        teller.add_special_offer(discount, catalog.products["toothbrush"])
        receipt = teller.checks_out_articles_from(cart)
        print("\n")
        print(ReceiptPrinter().print_receipt(receipt))
        self.assertAlmostEqual(receipt.total_price(), 6.875, places=2)
        self.assertEqual(1, len(receipt.discounts))
        self.assertEqual(2, len(receipt.items))


    def get_catalog_teller_and_cart_test_A(self, quantity_toothbrush):
        catalog = self.get_test_catalog()
        teller = Teller(catalog)
        cart = ShoppingCart()
        cart.add_item_quantity(catalog.products["apples"], 2.5)
        cart.add_item_quantity(catalog.products["toothbrush"], quantity_toothbrush)
        return catalog, teller, cart


def main():
    SupermarketTest().test_generic()
    SupermarketTest().test_ten_percent_discount()
    SupermarketTest().test_three_for_two_discount()
    SupermarketTest().test_three_for_two_discount_bis()
    SupermarketTest().test_five_for_amount()
    SupermarketTest().test_two_for_amount()

if __name__ == '__main__':
    unittest.main()
