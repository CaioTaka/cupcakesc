from flask import current_app


def calculate_shipping_cents(subtotal_cents):
    """Return the demo shipping charge for a cart subtotal."""
    config = current_app.config
    if subtotal_cents >= config["FREE_SHIPPING_FROM_CENTS"]:
        return 0
    if subtotal_cents > config["SHIPPING_REDUCED_FROM_CENTS"]:
        return config["SHIPPING_OVER_50_CENTS"]
    return config["SHIPPING_UP_TO_50_CENTS"]
