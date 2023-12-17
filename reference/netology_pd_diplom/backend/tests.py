from wsgiref import headers

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from backend.models import User, ConfirmEmailToken, Shop, Category
from rest_framework.authtoken.models import Token


# тест регистрации пользователя
class UserTestCase(APITestCase):
    def setUp(self):
        self.url = "/api/v1/"

        user1 = User.objects.create_user(
            first_name="NameBuyer",
            last_name="FamilyBuyer",
            email="Buyer@test.ru",
            password="PasswordBuyer",
            company="CompanyBuyer",
            position="PositionBuyer")
        user1.is_active = True


        user2 = User.objects.create(
            first_name="NameSeller",
            last_name="FamilySeller",
            email="Seller@test.ru",
            password="PasswordSeller",
            company="CompanySeller",
            position="PositionSeller",
            type="shop")
        user2.is_active = True

        self.token1 = Token.objects.create(user=user1)

        self.token2 = Token.objects.create(user=user2)

        Shop.objects.create(name='TestShop1')
        Shop.objects.create(name='TestShop2')

        Category.objects.create(name='TestCategory1')


    def test_user_login(self):
        """ Проверка авторизации """
        data = {
            'email': "Seller@test.ru",
            'password': "PasswordSeller"
        }
        response = self.client.post(self.url + 'user/login', data=data)

        self.assertEqual(response.status_code, 200)

    def test_get_list_shops(self):
        """ Проверка запроса списка магазинов """

        response = self.client.get(self.url + 'shops')
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data['results'], list)
        self.assertEqual(len(data['results']), 2)

    def test_get_list_categories(self):
        """ Проверка запроса списка категорий """

        response = self.client.get(self.url + 'categories')
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data['results'], list)
        self.assertEqual(len(data['results']), 1)


    # def test_user_register(self, **kwargs):
    #     data = {
    #         'first_name': "NameBuyer",
    #         'last_name': "FamilyBuyer",
    #         'email': "Buyer@test.ru",
    #         'password': "PasswordBuyer",
    #         'company': "CompanyBuyer",
    #         'position': "PositionBuyer"
    #         }
    #     response = self.client.post(self.url + 'user/register', **data)
    #     self.assertEqual(response.status_code, 201)



    def test_get_contacts_user(self):
        """ Проверка запроса контакта пользователя """

        response = self.client.get(self.url + 'user/contact',
            headers={'Authorization': 'Token ' + str(self.token1)})

        self.assertEqual(response.status_code, 200)
