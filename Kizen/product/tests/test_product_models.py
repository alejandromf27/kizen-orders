from django.test import TestCase
from product.models import Product


class ProductTestCase(TestCase):
    """ test product model """

    def test_product_integrity(self):
        """ test product model """
        prod = Product.objects.create(
            name='Product 1',
            description='Description of  the product 1',
            price=12.0
        )
        self.assertTrue(isinstance(prod, Product))
