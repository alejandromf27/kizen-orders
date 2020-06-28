from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from Kizen.response_data import json_data
from order.models.order import Order, OrderLine
from order.serializers.order import OrderSerializer, CustomizedOrderLineSerialized
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count


class ApiOrdersListView(ListAPIView):
    """
    ListAPIView to get orders
    """
    queryset = OrderLine.objects.all().order_by('order__number')
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = CustomizedOrderLineSerialized
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        customize the query by a search
        """
        queryset_list = self.queryset
        query = self.request.GET.get('q', False)
        user_id = self.request.GET.get('user', False)
        if query:
            queryset_list = queryset_list.filter(
                Q(order__number__icontains=query) |
                Q(order__user__email__icontains=query) |
                Q(product__name__icontains=query)
            )
        if user_id:
            queryset_list = queryset_list.filter(order__user_id=user_id)
        queryset_list = queryset_list.distinct()
        return queryset_list


class ManageOrderAPIView(APIView):
    """ class to manage order model objects"""

    permission_classes = [
        TokenHasReadWriteScope,  # access bearer token
    ]

    @staticmethod
    def post(request):
        """
        Create order
        :param request: http petition
        :return: order serialized data
        """
        try:
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(json_data(
                    data=serializer.data
                ), status=status.HTTP_201_CREATED)
            return Response(json_data(
                message=serializer.errors,
                status='danger'
            ), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(json_data(
                message=str(e),
                status='danger'
            ), status=status.HTTP_400_BAD_REQUEST)


class ApiOrdersProductsListView(APIView):
    """
    get query to get orders by restrictions
    """

    permission_classes = [TokenHasReadWriteScope]

    @staticmethod
    def get(request):
        """
        customize the query by a search
        """
        amount = request.GET.get('amount', 100)  # order total amount
        qty = request.GET.get('qty', 1)  # lines the order has
        queryset_list = Order.objects.all()
        # get all orders with total_price greater than "amount" and
        # has more than "qty" products
        orders = queryset_list.annotate(count=Count('lines')).filter(
            total_price__gt=amount,
            count__gt=qty
        )
        return Response(json_data(
            data=CustomizedOrderLineSerialized(
                instance=[line for order in orders for line in order.lines.all()], many=True
            ).data
        ), status=status.HTTP_200_OK)
