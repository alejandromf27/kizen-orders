from django.test import TestCase
from order.models.order import Order
from django.contrib.auth.models import User


class OrderTestCase(TestCase):
    """ test order model """

    def setUp(self):
        """ set up test environment with user """

        # create a user
        self.user = User.objects.create_user(username="jhon", password="any-password")

    def test_order_integrity(self):
        """ test order model"""
        order = Order.objects.create(
            number='00001',
            user=self.user
        )
        self.assertTrue(isinstance(order, Order))
