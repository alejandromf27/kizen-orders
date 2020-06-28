from rest_framework.test import APITestCase
from order.models.order import Order
from order.serializers.order import OrderSerializer
from django.contrib.auth.models import User


class OrderSerializerTestCase(APITestCase):
    """ order serializer test case """

    def setUp(self):
        """ set up the test case environment """
        # create a user
        self.user = User.objects.create_user(username="jhon", password="any-password")
        self.order_data = {
            'number': '00001',
            'user': self.user
        }
        self.order = Order.objects.create(**self.order_data)
        self.order_serializer = OrderSerializer(instance=self.order)

    def test_expected_data(self):
        """ test expected data in serializer """
        data = self.order_serializer.data
        self.assertEqual(
            set(data.keys()),
            {'number', 'user', 'lines'}
        )

    def test_field_name(self):
        """ test field name """
        data = self.order_serializer.data
        self.assertEqual(
            data['number'],
            self.order_data['number']
        )

    def test_field_user(self):
        """ test field user """
        data = self.order_serializer.data
        self.assertEqual(
            data['user'],
            self.order_data['user'].id
        )

    def test_serializer_valid_data(self):
        """ test valid data """
        serializer = OrderSerializer(data=self.order_serializer)
        self.assertFalse(serializer.is_valid())
