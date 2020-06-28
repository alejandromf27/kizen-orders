from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from kizen_user.serializers.user_serializer import get_access_token
from product.models import Product


class OrderWithAuthTestCase(APITestCase):
    """ test authenticated, order APIs """

    def setUp(self):
        """ set up test environment with authenticated user """

        # create a user
        self.user = User.objects.create_user(username="jhon", password="any-password")
        # generate a bearer token
        self.token = get_access_token(self.user)
        # pass credentials
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token['token'])

    def test_logged_list_orders(self):
        """ test API list of orders , expected http code 200"""
        response = self.client.get("/api/v1/orders/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_list_orders_search_key(self):
        """ test API list of orders , expected http code 200"""
        response = self.client.get("/api/v1/orders/list/?q=AA")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_list_orders_filter_by_user(self):
        """ test API list of orders , expected http code 200"""
        response = self.client.get("/api/v1/orders/list/?user=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_list_products_orders_condition(self):
        """
        test API list of products in a order with amount greater than a value,
        and more than a Y number of products,
        expected http code 200
        """
        response = self.client.get("/api/v1/orders/products/?amount=100&qty=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_create_order(self):
        """ test create an order , expected http code 201"""
        user = User.objects.create_user(username="bill", password="any-password")
        prod1 = Product.objects.create(
            name='Product 1',
            description='Description of  the product 1',
            price=12.0
        )
        prod2 = Product.objects.create(
            name='Product 2',
            description='Description of  the product 2',
            price=12.0
        )
        data = {
            "user": user.id,
            "lines": [
                {
                    "product": prod1.id,
                    "quantity": 2
                },
                {
                    "product": prod2.id,
                    "quantity": 5
                }
            ]
        }
        response = self.client.post("/api/v1/orders/manage/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_create_order_missing_required(self):
        """ test create an order , expected http code 400"""
        user = User.objects.create_user(username="bill", password="any-password")
        prod2 = Product.objects.create(
            name='Product 2',
            description='Description of  the product 2',
            price=12.0
        )
        data = {
            "user": user.id,
            "lines": [
                {
                    "quantity": 2
                },
                {
                    "product": prod2.id,
                    "quantity": 5
                }
            ]
        }
        response = self.client.post("/api/v1/orders/manage/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderWithoutAuthTestCase(APITestCase):
    """
        test non authenticated, order APIs
        expected http code 401
        """

    def test_non_logged_list_orders(self):
        """ try to access to API without authentication """
        response = self.client.get("/api/v1/orders/list/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_logged_create_order(self):
        """ test create an order , expected http code 401"""
        user = User.objects.create_user(username="bill", password="any-password")
        prod1 = Product.objects.create(
            name='Product 1',
            description='Description of  the product 1',
            price=12.0
        )
        prod2 = Product.objects.create(
            name='Product 2',
            description='Description of  the product 2',
            price=12.0
        )
        data = {
            "user": user.id,
            "lines": [
                {
                    "product": prod1.id,
                    "quantity": 2
                },
                {
                    "product": prod2.id,
                    "quantity": 5
                }
            ]
        }
        response = self.client.post("/api/v1/orders/manage/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
