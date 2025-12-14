from model_objects import ProductQuantity


class ShoppingCart:

    def __init__(self):
        self._items = []
        self._product_quantities_prices = {}

    def set_prices(self, catalog):
        for product in self._product_quantities_prices.keys():
            self._product_quantities_prices[product]["price"] = catalog.unit_price(product)

    @property
    def items(self):
        return self._items

    def add_item(self, product):
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self):
        return self._product_quantities_prices

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities_prices.keys():
            self._product_quantities_prices[product]["quantity"] = self._product_quantities_prices[product]["quantity"] + quantity
        else:
            self._product_quantities_prices[product] = {"quantity": quantity,
                                                        "price": None}
    def get_quantity(self, product):
        return self._product_quantities_prices[product]["quantity"]

    def get_price(self, product):
        return self._product_quantities_prices[product]["price"]

    def get_products(self):
        return self._product_quantities_prices.keys()

    def get_product_quantities_prices(self, products):
        return {self._product_quantities_prices[key] for key in products}

    def add_products_to_recipe(self, receipt):
        for product in self.get_products():
            quantity = self.get_quantity(product)
            unit_price = self.get_price(product)
            price = quantity * unit_price
            receipt.add_product(product, quantity, unit_price, price)







