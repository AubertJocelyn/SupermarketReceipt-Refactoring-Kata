from model_objects import ProductUnit


class ReceiptPrinter:

    def __init__(self, columns=40):
        self.columns = columns

    def print_receipt(self, receipt):
        print("\n")
        result = ""
        result += self.get_products_lines(receipt)
        result += self.get_discounts_lines(receipt)
        result += self.get_tickets_lines(receipt)
        result += self.print_fidelity_points(receipt)
        result += self.present_total(receipt)
        return str(result)

    def get_products_lines(self, receipt):
        output = "Products:\n"
        for item in receipt.items:
            receipt_item = self.print_receipt_item(item)
            output += receipt_item
        return output

    def get_discounts_lines(self, receipt):
        output = ""
        if receipt.discounts:
            output += ("\n" + "Discounts:" + "\n")
        for discount in receipt.discounts:
            discount_presentation = self.print_discount(discount)
            output += discount_presentation
        return output

    def get_tickets_lines(self, receipt):
        output = ""
        if receipt._ticket_discounts:
            output += ("\n" + "Ticket discounts:" + "\n")
        for ticket_discount in receipt._ticket_discounts:
            discount_presentation = self.print_discount(ticket_discount)
            output += discount_presentation
        return output

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
            name = name[:len(name) - 1]
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

    def print_discount(self, discount):
        output = ""
        messages = discount.get_message()
        products = discount.products
        for i in range(len(messages)):
            name = f"{messages[i]} ({products[i].name})"
            value = ""
            output += self.format_line_with_whitespace(name, value)
        output += self.format_line_with_whitespace("", self.print_price(discount.discount_amount))
        return output

    def present_total(self, receipt):
        name = "Total: "
        value = self.print_price(receipt.total_price())
        return "\n" + self.format_line_with_whitespace(name, value)

    def print_fidelity_points(self, receipt):
        output = "\nFidelity Points:\n"
        names = ["fidelity points used", "fidelity points gained", "fidelity points count"]
        values = [receipt.fidelity_points_used, receipt.fidelity_points_gained, receipt.fidelity_points_count]
        for i in range(len(names)):
            output += self.format_line_with_whitespace(names[i], f"{values[i]:.2f}")
        return output
