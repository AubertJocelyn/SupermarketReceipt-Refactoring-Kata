from model_objects import ProductQuantity, SpecialOfferType, Discount

def main(cart, receipt, offers, catalog):
    for p in cart._product_quantities.keys():
        if p in offers.keys():
            discount = get_discount(p, quantity=cart._product_quantities[p], offer=offers[p],
                                         unit_price=catalog.unit_price(p))
            if discount:
                receipt.add_discount(discount)


def get_discount(p, quantity, offer, unit_price):
    if offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
        return get_discount_x_for_amount(p, quantity, unit_price, offer.argument, 2)

    elif offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
        return get_discount_x_for_amount(p, quantity, unit_price, offer.argument, 5)

    elif offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
        return get_discount_x_for_amount(p, quantity, unit_price, 2 * unit_price, 3)

    elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
        return get_discount_x_for_amount(p, quantity, unit_price, 0.9 * unit_price, 1)
    else:
        return None


def get_discount_x_for_amount(p, quantity, unit_price, amount, x):
    total = amount * (int(quantity) // x) + int(quantity) % x * unit_price
    discount_total = unit_price * quantity - total
    if discount_total == 0.0:
        return None
    discount = Discount(p, str(x) + " for " + str(amount), -discount_total)
    return discount