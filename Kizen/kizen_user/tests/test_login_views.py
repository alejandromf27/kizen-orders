from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from kizen_user.serializers.user_serializer import get_access_token


class LoginUserTestCase(APITestCase):
    """
    test class to check auth user
    """

    def test_login(self):
        """
        Test the login functionality
        """
        # crete a sample user
        User.objects.create_user(username="jhon", password="123456")
        # try then login by the API
        response = self.client.post("/api/v1/user/login/", {'username': "jhon", 'password': "123456"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_failed(self):
        """
        Test the login functionality top failed
        """
        # crete a sample user
        User.objects.create_user(username="jhon", password="123456")
        # try then login by the API qith wrong credentials
        response = self.client.post("/api/v1/user/login/", {'username': "jhon", 'password': "12"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutUserTestCase(APITestCase):
    """ logout user test case """

    def setUp(self):
        """ set up the test case environment with a logged user"""

        # create a user
        self.user = User.objects.create_user(username="jhon", password="any-password")
        # generate a bearer token
        self.token = get_access_token(self.user)
        # pass credentials
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token['token'])

    def test_logout(self):
        """ test logout api """
        response = self.client.post("/api/v1/user/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_wrong_token(self):
        """ test logout api with a wrong bearer token """

        # set token
        any_token = "any-wrong-token"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + any_token)
        # check api logout
        response = self.client.post("/api/v1/user/logout/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
