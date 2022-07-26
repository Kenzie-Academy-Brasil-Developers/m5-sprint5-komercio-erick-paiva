from django.test import TestCase
from users.models import User
from products.models import Product


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.description = "apple"
        cls.price = 15.99
        cls.quantity = 10
        cls.mock_seller = User.objects.create(
            email="seller@mail.com",
            password="1234",
            first_name="Jhon",
            last_name="Doe",
            is_seller=True,
        )

        cls.mock_product = Product.objects.create(
            description="apple", price=15.99, quantity=10, seller=cls.mock_seller
        )

    def test_product_fields(self):
        self.assertIsInstance(self.mock_product.description, str)
        self.assertEqual(self.mock_product.price, self.price)
        self.assertIsInstance(self.mock_product, Product)

    def test_if_the_seller_is_the_same_that_created_it(self):
        self.assertTrue(self.mock_product.seller == self.mock_seller)
