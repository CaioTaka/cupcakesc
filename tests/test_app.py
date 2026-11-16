import sqlite3
import tempfile
import unittest
from pathlib import Path

from app import create_app


class CupcakesAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database = Path(self.temp_dir.name) / "test.sqlite3"
        self.app = create_app({"TESTING": True, "DATABASE": str(database), "SECRET_KEY": "test-secret"})
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def set_cart(self, client, items):
        with client.session_transaction() as session:
            session["cart"] = items

    @staticmethod
    def demo_single():
        return {
            "kind": "single",
            "flavor_id": "baunilha",
            "name": "Baunilha",
            "quantity": 1,
            "unit_price_cents": 1000,
        }

    def make_order(self, client, payment_method="credit"):
        self.set_cart(client, [self.demo_single()])
        response = client.post("/order/confirm", data={"payment_method": payment_method})
        self.assertEqual(response.status_code, 302)
        return response.headers["Location"]

    def test_catalog_and_footer_are_available_on_catalog_only(self):
        home = self.client.get("/")
        catalog = self.client.get("/catalog")
        self.assertEqual(home.status_code, 200)
        self.assertNotIn(b"Projeto Integrador Transdisciplinar II", home.data)
        self.assertEqual(catalog.status_code, 200)
        self.assertIn(b"Projeto Integrador Transdisciplinar II", catalog.data)

    def test_combo_requires_exact_quantity_and_can_be_edited(self):
        invalid = self.client.post("/combos/6", data={"flavor_baunilha": "5"})
        self.assertEqual(invalid.status_code, 200)
        with self.client.session_transaction() as session:
            self.assertEqual(session.get("cart", []), [])

        added = self.client.post(
            "/combos/6",
            data={"flavor_baunilha": "3", "flavor_chocolate": "3"},
        )
        self.assertEqual(added.status_code, 302)
        edited = self.client.post(
            "/combos/6",
            data={"edit_index": "0", "flavor_baunilha": "1", "flavor_chocolate": "5"},
        )
        self.assertEqual(edited.status_code, 302)
        with self.client.session_transaction() as session:
            combo = session["cart"][0]
            self.assertEqual(combo["flavors"], [
                {"id": "baunilha", "name": "Baunilha", "quantity": 1},
                {"id": "chocolate", "name": "Chocolate", "quantity": 5},
            ])

    def test_payment_method_is_saved_and_shown_in_order_history(self):
        tracking_path = self.make_order(self.client, "pix")
        history = self.client.get("/order/history")
        tracking = self.client.get(tracking_path)
        self.assertEqual(history.status_code, 200)
        self.assertIn(b"Pix", history.data)
        self.assertIn(b"Pagamento", tracking.data)
        self.assertIn(b"Pix", tracking.data)

        database = self.app.config["DATABASE"]
        db = sqlite3.connect(database)
        try:
            method = db.execute("SELECT payment_method FROM orders").fetchone()[0]
        finally:
            db.close()
        self.assertEqual(method, "pix")

    def test_order_history_is_separated_between_browser_sessions(self):
        self.make_order(self.client, "debit")
        other_browser = self.app.test_client()
        history = other_browser.get("/order/history")
        self.assertIn(b"Seus pedidos", history.data)
        self.assertNotIn(b"Pedido #1", history.data)

    def test_tracking_updates_without_full_page_reload(self):
        tracking_path = self.make_order(self.client)
        page = self.client.get(tracking_path)
        self.assertIn(b"fetch(pollUrl", page.data)
        self.assertNotIn(b"window.location.reload", page.data)
        progress = self.client.get(tracking_path + "/progress")
        self.assertEqual(progress.status_code, 200)
        self.assertIn("stage", progress.get_json())

    def test_shipping_tiers_are_consistent_in_cart_and_checkout(self):
        cases = [
            (5000, "R$ 15,00"),
            (5001, "R$ 5,00"),
            (15000, "Grátis"),
        ]
        for subtotal, expected_shipping in cases:
            with self.subTest(subtotal=subtotal):
                item = self.demo_single()
                item["unit_price_cents"] = subtotal
                self.set_cart(self.client, [item])

                cart = self.client.get("/cart")
                checkout = self.client.get("/order/checkout")
                self.assertIn(expected_shipping, cart.get_data(as_text=True))
                self.assertIn(expected_shipping, checkout.get_data(as_text=True))

    def test_adding_single_cupcake_returns_to_selected_card(self):
        response = self.client.post("/cart/add/oreo")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/catalog?adicionado=oreo#cupcake-oreo")

        catalog = self.client.get("/catalog?adicionado=oreo")
        self.assertIn('id="cupcake-oreo"', catalog.get_data(as_text=True))
        self.assertIn("Adicionado ao carrinho", catalog.get_data(as_text=True))

    def test_profile_has_accessible_theme_switch(self):
        profile = self.client.get("/profile")
        self.assertEqual(profile.status_code, 200)
        self.assertIn(b'role="switch"', profile.data)
        self.assertIn(b"Ativar tema escuro", profile.data)


if __name__ == "__main__":
    unittest.main()
