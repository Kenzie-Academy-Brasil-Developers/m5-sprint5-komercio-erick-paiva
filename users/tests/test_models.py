from django.test import TestCase
from users.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.first_name = "Jhon"
        cls.last_name = "Doe"
        cls.email = "jhon@gmail.com"
        cls.is_seller = True
        cls.password = "1234"

        cls.mock_user = User.objects.create(
            email="jhon@mail.com",
            password="1234",
            first_name="Jhon",
            last_name="Doe",
            is_seller=True,
        )

    def test_if_the_user_is_a_seller(self):
        self.assertEquals(self.mock_user.is_seller, True)

    def test_if_user_is_active_by_default(self):
        self.assertEquals(self.mock_user.is_active, True)

    def test_user_fields(self):
        self.assertIsInstance(self.mock_user.first_name, str)
        self.assertEqual(self.mock_user.first_name, self.first_name)
        self.assertIsInstance(self.mock_user.password, str)
        self.assertIsInstance(self.mock_user, AbstractUser)
