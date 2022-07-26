from rest_framework.test import APITestCase
from products.models import Product
from users.models import User
from rest_framework.authtoken.models import Token


class ProductViewTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create(
            email="super@mail.com",
            password="1234",
            first_name="Jhon",
            last_name="Doe",
            is_seller=True,
            is_superuser=True,
        )

        self.seller_user = User.objects.create(
            email="seller@mail.com",
            password="1234",
            first_name="Jhon",
            last_name="Doe",
            is_seller=True,
        )

        self.created_mock_product = Product.objects.create(
            description="Iphone 20",
            price=9999999,
            quantity=100000,
            seller=self.seller_user,
        )

    @classmethod
    def setUpTestData(cls):
        cls.url = "/api/products/"
        cls.mock_product = {
            "description": "Iphone 20",
            "price": 9999999,
            "quantity": 100000,
        }

    def test_create_product(self):
        self.token = Token.objects.create(user=self.seller_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(self.url, self.mock_product)

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_create_product_fail(self):
        response = self.client.post(self.url, self.mock_product)

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("id", response.json())

    def test_get_all_products(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) >= 0)

    def test_get_only_one_product(self):
        response = self.client.get(f"/api/products/{self.created_mock_product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("description", response.json())

    def test_get_only_one_product_404(self):
        response = self.client.get("/api/products/999/")
        self.assertEqual(response.status_code, 404)
        self.assertNotIn("description", response.json())

    def test_update_a_product(self):
        self.token = Token.objects.create(user=self.seller_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.patch(f"/api/products/{self.created_mock_product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("description", response.json())

    def test_update_a_product_401(self):
        response = self.client.patch(f"/api/products/{self.created_mock_product.id}/")
        self.assertEqual(response.status_code, 401)
        self.assertNotIn("description", response.json())
        self.assertDictEqual(
            response.json(), {"detail": "Authentication credentials were not provided."}
        )

    def try_to_update_a_product_from_another_seller_403(self):
        self.token = Token.objects.create(user=self.seller_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.patch(f"/api/products/{self.created_mock_product.id}/")
        self.assertEqual(response.status_code, 403)
        self.assertNotIn("description", response.json())
        self.assertDictEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )
