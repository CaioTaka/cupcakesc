from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = "chave-local-apenas-para-demo"
    DATABASE = str(BASE_DIR / "instance" / "cupcakesc.sqlite3")
    APP_NAME = "Cupcakes C"

    # Dados fixos e fictícios usados apenas na demonstração.
    DEMO_CUSTOMER_NAME = "Cliente"
    DEMO_CUSTOMER_EMAIL = "cliente@cupcakesc.com"
    DEMO_CARD_LAST4 = "1234"
    PICKUP_ADDRESS = "Shopping Vale Sul, São José dos Campos - SP"
    DELIVERY_ADDRESS = "Prefeitura de São José dos Campos - SP"
    PIX_DEMO_KEY = "cupcakesc123"
    ORDER_AUTO_ACCEPT_SECONDS = 5
    PREPARATION_SECONDS = 15
    DELIVERY_ESTIMATE_SECONDS = 30
    SHIPPING_UP_TO_50_CENTS = 1500
    SHIPPING_OVER_50_CENTS = 500
    SHIPPING_REDUCED_FROM_CENTS = 5000
    FREE_SHIPPING_FROM_CENTS = 15000

    # Catálogo e preços ficam centralizados aqui para facilitar alterações.
    COMBOS = [
        {"units": 6, "name": "Caixa com 6 Cupcakes", "description": "6 unidades variadas", "price_cents": 6000, "image": "combo-6-cupcakes.png"},
        {"units": 15, "name": "Caixa com 15 Cupcakes", "description": "15 unidades variadas", "price_cents": 15000, "image": "combo-15-cupcakes.png"},
    ]
    CUPCAKES = [
        {"id": "baunilha", "name": "Baunilha", "price_cents": 1000, "image": "cupcake-baunilha.png"},
        {"id": "chocolate", "name": "Chocolate", "price_cents": 1000, "image": "cupcake-chocolate.png"},
        {"id": "doce-de-leite", "name": "Doce de Leite", "price_cents": 1000, "image": "cupcake-doce-de-leite.png"},
        {"id": "brigadeiro", "name": "Brigadeiro", "price_cents": 1000, "image": "cupcake-brigadeiro.png"},
        {"id": "morango", "name": "Morango", "price_cents": 1000, "image": "cupcake-morango.png"},
        {"id": "oreo", "name": "Oreo", "price_cents": 1000, "image": "cupcake-oreo.png"},
    ]
