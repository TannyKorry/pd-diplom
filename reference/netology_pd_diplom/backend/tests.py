from wsgiref import headers

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from backend.models import User, ConfirmEmailToken, Shop, Category, Product, ProductInfo, Order
from rest_framework.authtoken.models import Token



class UserTestCase(APITestCase):
    def setUp(self):
        self.url = "/api/v1/"

        self.user1 = User.objects.create_user(
            first_name="NameBuyer",
            last_name="FamilyBuyer",
            email="Buyer@test.ru",
            password="PasswordBuyer",
            company="CompanyBuyer",
            position="PositionBuyer")
        self.user1.is_active = True
        self.user1.save()
        self.token1 = Token.objects.create(user=self.user1)


        self.user2 = User.objects.create(
            first_name="NameSeller",
            last_name="FamilySeller",
            email="Seller@test.ru",
            password="PasswordSeller",
            company="CompanySeller",
            position="PositionSeller",
            type="shop")
        self.user2.is_active = True
        self.user2.save()
        self.token2 = Token.objects.create(user=self.user2)

        Shop.objects.create(id=1, name='TestShop1')

        Category.objects.create(name='TestCategory1')
        Category.objects.create(name='TestCategory2')


    def test_user_register(self):
        """ Проверка регистрации пользователя """

        data = {
            'first_name': "NameBuyer",
            'last_name': "FamilyBuyer",
            'email': "Buyer@test.ru",
            'password': "PasswordBuyer",
            'company': "CompanyBuyer",
            'position': "PositionBuyer"
            }
        response = self.client.post(self.url + 'user/register', data=data, format='json')
        self.assertEqual(response.status_code, 201)


    def test_get_contacts_user(self):
        """ Проверка запроса контакта пользователя """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token1))
        response = self.client.get(self.url + 'user/contact')

        self.assertEqual(response.status_code, 200)


    def test_create_contacts_user(self):
        """ Проверка создания контакта пользователя """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token1))
        user = User.objects.get(auth_token=self.token1)

        contact1 = {
            'user_id': user.id,
            'city': "Almaty",
            'street': "Shashkin",
            'house': 28,
            'apartment': 123,
            'phone': '+ 49564563242'
        }

        response = self.client.post(self.url + 'user/contact', data=contact1)
        print(User.objects.get(auth_token=self.token1))
        self.assertEqual(response.status_code, 200)


    def test_user_login(self):
        """ Проверка авторизации """
        data = {
            'email': "Seller@test.ru",
            'password': "PasswordSeller"
        }

        response = self.client.post(self.url + 'user/login', data=data, format='json')

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


    def test_get_partner_order(self):
        """ Тестирование получения магазином размещенных заказов """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token2))

        user = User.objects.get(auth_token=self.token2)
        response = self.client.get(self.url + 'partner/orders')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.type, 'shop')



    def test_get_partner_order_only_shop(self):
        """
        Тестирование получения магазином размещенных заказов
        (заказы может получить только магазин)
        """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token1))

        user = User.objects.get(auth_token=self.token1)
        response = self.client.get(self.url + 'partner/orders')

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(user.type, 'shop')


