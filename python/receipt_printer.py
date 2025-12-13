from Offers.Bundle import Bundle, UniformXPercentDiscountBundle
from Offers.SimpleDiscount import SimpleDiscount
from model_objects import ProductUnit

class ReceiptPrinter:

    def __init__(self, columns=40):
        self.columns = columns
  
    def print_receipt(self, receipt):
        result = "Products:\n"
        for item in receipt.items:
            receipt_item = self.print_receipt_item(item)
            result += receipt_item
        result += ("\n" + "Discounts:" + "\n")
        for discount in receipt.discounts:
            discount_presentation = self.choose_print_discount(discount)
            result += discount_presentation
        if receipt._ticket_discounts:
            result += ("\n" + "Ticket discounts:" + "\n")
        for ticket_discount in receipt._ticket_discounts:
            discount_presentation = self.choose_print_discount(ticket_discount)
            result += discount_presentation

        result += "\n"
        result += self.present_total(receipt)
        return str(result)

    def print_receipt_item(self, item):
        total_price_printed = self.print_price(item.total_price)
        name = item.product.name
        line = self.format_line_with_whitespace(name, total_price_printed)
        if item.quantity != 1:
            line += f"  {self.print_price(item.price)} * {self.print_quantity(item)}\n"
        return line

    def format_line_with_whitespace(self, name, value):
        whitespace_size = self.columns - len(name) - len(value)
        while whitespace_size < 1:
            name = name[:len(name)-1]
            whitespace_size = self.columns - len(name) - len(value)
        line = name
        for i in range(whitespace_size):
            line += " "
        line += value
        line += "\n"
        return line

    def print_price(self, price):
        return "%.2f" % price

    def print_quantity(self, item):
        if ProductUnit.EACH == item.product.unit:
            return str(item.quantity)
        else:
            return '%.3f' % item.quantity

    def choose_print_discount(self, discount):
        if isinstance(discount, SimpleDiscount):
            return self.print_simple_discount(discount)
        elif isinstance(discount, Bundle):
            return self.print_bundle_discount(discount)

    def print_simple_discount(self, simple_discount):
        name = f"{simple_discount.get_message()} ({simple_discount.product.name})"
        value = self.print_price(simple_discount.discount_amount)
        return self.format_line_with_whitespace(name, value)

    def print_bundle_discount(self, bundle_discount):
        output = ""
        messages = bundle_discount.get_message()
        products = bundle_discount.products
        for i in range(len(messages)):
            name = f"{messages[i]} ({products[i].name})"
            value = ""
            output += self.format_line_with_whitespace(name, value)
        output += self.format_line_with_whitespace("", self.print_price(bundle_discount.discount_amount))
        return output

    def present_total(self, receipt):
        name = "Total: "
        value = self.print_price(receipt.total_price())
        return self.format_line_with_whitespace(name, value)
