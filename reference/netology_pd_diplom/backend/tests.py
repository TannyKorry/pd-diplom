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
        user1.save()
        self.token1 = Token.objects.create(user=user1)

        user2 = User.objects.create(
            first_name="NameSeller",
            last_name="FamilySeller",
            email="Seller@test.ru",
            password="PasswordSeller",
            company="CompanySeller",
            position="PositionSeller",
            type="shop")
        user2.is_active = True
        user2.save()
        self.token2 = Token.objects.create(user=user2)

        Shop.objects.create(name='TestShop1')

        Category.objects.create(name='TestCategory1')
        Category.objects.create(name='TestCategory2')

    # def test_user_register(self):
    #     """ Проверка регистрации пользователя """
    #
    #     data = {
    #         'first_name': "NameBuyer",
    #         'last_name': "FamilyBuyer",
    #         'email': "Buyer@test.ru",
    #         'password': "PasswordBuyer",
    #         'company': "CompanyBuyer",
    #         'position': "PositionBuyer"
    #         }
    #     response = self.client.post(self.url + 'user/register', data=data, format='json')
    #     self.assertEqual(response.status_code, 201)

    def test_get_contacts_user(self):
        """ Проверка запроса контакта пользователя """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token1))
        response = self.client.get(self.url + 'user/contact')

        self.assertEqual(response.status_code, 200)

    # def test_create_contacts_user(self):
    #     """ Проверка создания контакта пользователя """
    #     data = {
    #         'city': "Almaty",
    #         'street': "Shashkin",
    #         'house': 28,
    #         'apartment': 123,
    #         'phone': '+ 49564563242'
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token1))
    #     response = self.client.post(self.url + 'user/contact', data=data, )
    #
    #     self.assertEqual(response.status_code, 201)


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
        self.assertEqual(len(data['results']), 1)


    def test_get_list_categories(self):
        """ Проверка запроса списка категорий """

        response = self.client.get(self.url + 'categories')
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data['results'], list)
        self.assertEqual(len(data['results']), 2)






