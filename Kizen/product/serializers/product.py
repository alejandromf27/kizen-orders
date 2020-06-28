from rest_framework import serializers
from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """ serialize to json Product objects"""

    image = serializers.ImageField(required=False)
    image_path = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'is_active', 'image', 'image_path', 'price')

    @staticmethod
    def get_image_path(obj):
        """
        get the image relative route
        """
        return obj.image.url if obj.image else None
