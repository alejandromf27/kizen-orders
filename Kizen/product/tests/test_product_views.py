from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from kizen_user.serializers.user_serializer import get_access_token


class ProductWithAuthTestCase(APITestCase):
    """ test authenticated, product APIs """

    def setUp(self):
        """ set up test environment with authenticated user """

        # create a user
        self.user = User.objects.create_user(username="jhon", password="any-password")
        # generate a bearer token
        self.token = get_access_token(self.user)
        # pass credentials
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token['token'])

    def test_logged_list_product(self):
        """ test API list of products , expected http code 200"""
        response = self.client.get("/api/v1/products/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_create_product(self):
        """ test API list of products , expected http code 201"""
        data = {
            'name': 'Prod1',
            'description': 'Prod1 my descrption',
            'price': 10.0
        }
        response = self.client.post("/api/v1/products/manage/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_create_product_missing_required(self):
        """ test API list of products , expected http code 201"""
        data = {
            'description': 'Prod1 my descrption',
            'price': 10.0
        }
        response = self.client.post("/api/v1/products/manage/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductWithoutAuthTestCase(APITestCase):
    """
        test non authenticated, product APIs
        expected http code 401
        """

    def test_non_logged_list_product(self):
        """ try to access to API without authentication """
        response = self.client.get("/api/v1/products/list/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_logged_create_product(self):
        """ test API list of products , expected http code 401"""
        data = {
            'name': 'Prod1',
            'description': 'Prod1 my descrption',
            'price': 10.0
        }
        response = self.client.post("/api/v1/products/manage/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
