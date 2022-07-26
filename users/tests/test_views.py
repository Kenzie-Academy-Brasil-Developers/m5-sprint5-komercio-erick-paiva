from rest_framework.test import APITestCase
from users.models import User
from rest_framework.authtoken.models import Token


class UserViewTest(APITestCase):
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

    @classmethod
    def setUpTestData(cls):
        cls.url = "/api/accounts/"
        cls.mock_user = {
            "email": "jhon@mail.com",
            "password": "1234",
            "first_name": "Jhon",
            "last_name": "Doe",
            "is_seller": False,
        }
        cls.mock_seller_user = {
            "email": "selleruser@mail.com",
            "password": "1234",
            "first_name": "Jhon",
            "last_name": "Doe",
            "is_seller": True,
        }
        cls.invalid_mock_user = {
            "password": "1234",
            "first_name": "Jhon",
            "last_name": "Doe",
        }

    def test_create_user(self) -> None:
        response = self.client.post(self.url, self.mock_user)

        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.json())
        self.assertIn("email", response.json())

    def test_create_seller_user(self) -> None:
        response = self.client.post(self.url, self.mock_seller_user)

        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.json())
        self.assertIn("email", response.json())

    def test_create_user_fails(self) -> None:
        response = self.client.post(self.url, self.invalid_mock_user)

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.json(),
            {"email": ["This field is required."]},
        )

    def test_list_newest_users(self):
        response = self.client.get("/api/accounts/newest/1/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) >= 0)

    def test_by_editing_the_user(self):
        self.token = Token.objects.create(user=self.seller_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.patch(
            f"/api/accounts/{self.seller_user.id}/",
            {
                "first_name": "Mike",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("first_name", response.json())


class LoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = "/api/login/"
        cls.mock_user = {
            "email": "jhon@mail.com",
            "password": "1234",
            "first_name": "Jhon",
            "last_name": "Doe",
            "is_seller": True,
        }
        cls.invalid_mock_user = {
            "email": "jhon@mail.com",
            "password": "12345",
            "first_name": "Jhon",
            "last_name": "Doe",
            "is_seller": False,
        }

    def setUp(self) -> None:
        User.objects.create_user(**self.mock_user)

    def test_login(self):
        response = self.client.post(self.url, self.mock_user)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_fail_invalid_credentials(self):
        response = self.client.post(self.url, self.invalid_mock_user)

        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            response.json(),
            {"error": "Email or password is incorrect"},
        )

    def test_login_fail_invalid_body(self):
        response = self.client.post(self.url, {"email": "email"})

        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.json())
