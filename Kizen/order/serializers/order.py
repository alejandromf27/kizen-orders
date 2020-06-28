from rest_framework import serializers
from order.models.order import Order, OrderLine
from product.serializers.product import ProductSerializer


class OrderLineSerializer(serializers.ModelSerializer):
    """ serializer to json order line obj """

    class Meta:
        model = OrderLine
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    """ serialize to json Order objects"""

    number = serializers.SerializerMethodField()
    lines = OrderLineSerializer(many=True)

    class Meta:
        model = Order
        fields = ('number', 'user', 'lines')

    @staticmethod
    def get_number(obj):
        return obj.__str__()

    @staticmethod
    def get_user_name(obj):
        return obj.user.email

    @staticmethod
    def get_total_price(obj):
        return obj.total_price

    def create(self, validated_data):
        """ rewrite the create method to add lines of the order"""
        lines_data = validated_data.pop('lines')
        order = Order.objects.create(**validated_data)
        total_price = 0
        for line_data in lines_data:
            line = OrderLine.objects.create(order=order, **line_data)
            total_price += line.subtotal_price
        # update total order price after create each lines
        order.total_price = total_price
        order.save()
        return order


class CustomizedOrderLineSerialized(serializers.ModelSerializer):
    """ customized serialized for order lines to show in a report """

    number = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderLine
        fields = ('number', 'product_name')

    @staticmethod
    def get_number(obj):
        return obj.order.__str__()

    @staticmethod
    def get_product_name(obj):
        return obj.product.name
