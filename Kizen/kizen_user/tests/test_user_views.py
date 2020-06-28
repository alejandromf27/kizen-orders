from rest_framework.test import APITestCase
from rest_framework import status


class UserAPIWithAuthTestCase(APITestCase):
    """ test user registration"""

    def test_register_user(self):
        """ test api to create users , expect http code 201"""
        data = {
            "user": {
                "email": "pepito3324@gmail.com",
                "password": "123456"
            },
            "birth_date": "1947-09-23"
        }
        # hit the api with the correct data
        response = self.client.post("/api/v1/user/register/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_non_required_field(self):
        """
        test api to create user
        missing a required field value (email)
        expected http code 400
        """
        data = {
            "user": {
                "password": "123456"
            },
            "birth_date": "1947-09-23"
        }
        response = self.client.post("/api/v1/user/register/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_non_required_pass(self):
        """
        test api to create user
        missing a required field value (password)
        expected http code 400
        """
        data = {
            "user": {
                "email": "pepito3324@gmail.com"
            },
            "birth_date": "1947-09-23"
        }
        response = self.client.post("/api/v1/user/register/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
