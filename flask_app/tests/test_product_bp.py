import unittest
from app import app


class ProductBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_list(self):
        """Тест маршруту /products/."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Список продуктів", response.data.decode('utf-8'))

    def test_product_detail(self):
        """Тест маршруту /products/<product_id>."""
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Продукт 1", response.data.decode('utf-8'))


if __name__ == "__main__":
    unittest.main()