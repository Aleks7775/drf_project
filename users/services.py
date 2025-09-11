import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Создание продукта на страйпе"""
    return stripe.Product.create(
        name=product.title
    )


def create_stripe_price(amount, product):
    """Создает цену на страйпе"""

    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product.id,
    )


def create_stripe_session(price):
    """Ссылка на оплату"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
