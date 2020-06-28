from rest_framework.test import APITestCase
from product.models import Product
from product.serializers.product import ProductSerializer


class ProductSerializerTestCase(APITestCase):
    """ product serializer test case """

    def setUp(self):
        """ set up the test case environment """
        self.product_data = {
            'name': 'My first product',
            'description': 'my description',
            'is_active': True,
            'image': None,
            'price': 10.0
        }
        self.product = Product.objects.create(**self.product_data)
        self.product_serializer = ProductSerializer(instance=self.product)

    def test_expected_data(self):
        """ test expected data in serializer """
        data = self.product_serializer.data
        self.assertEqual(
            set(data.keys()),
            set(['id', 'name', 'description', 'is_active', 'image', 'image_path', 'price'])
        )

    def test_field_name(self):
        """ test field name """
        data = self.product_serializer.data
        self.assertEqual(
            data['name'],
            self.product_data['name']
        )

    def test_field_image(self):
        """ test field image """
        data = self.product_serializer.data
        self.assertEqual(
            data['image'],
            self.product_data['image']
        )

    def test_serializer_valid_data(self):
        """ test valid data """
        serializer = ProductSerializer(data=self.product_serializer)
        self.assertFalse(serializer.is_valid())
