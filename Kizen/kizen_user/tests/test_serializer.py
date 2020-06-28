from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from kizen_user.serializers.user_serializer import UserSimpleSerializer


class UserSerializerTestCase(APITestCase):
    """ user serializer test case """

    def setUp(self):
        """ set up the test case environment """
        self.user_data = {
            'email': 'bcolleman@gmail.com',
            'password': 'any-pass'
        }
        self.user = User.objects.create(**self.user_data)
        self.user_serializer = UserSimpleSerializer(instance=self.user)

    def test_expected_data(self):
        """ test expected data in serializer """
        data = self.user_serializer.data
        self.assertEqual(
            set(data.keys()),
            {'email', 'password'}
        )

    def test_field_email(self):
        """ test field email """
        data = self.user_serializer.data
        self.assertEqual(
            data['email'],
            self.user_data['email']
        )

    def test_serializer_valid_data(self):
        """ test valid serializer data """
        serializer = UserSimpleSerializer(data=self.user_serializer)
        self.assertFalse(serializer.is_valid())
