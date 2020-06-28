from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from Kizen.response_data import json_data
from product.models import Product
from product.serializers.product import ProductSerializer
from rest_framework.pagination import PageNumberPagination


class ApiProductsListView(ListAPIView):
    """
    ListAPIView to get products
    """
    queryset = Product.objects.all().order_by('name')
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        customize the query by a search
        """
        queryset_list = self.queryset
        query = self.request.GET.get('q', False)
        if query:
            queryset_list = queryset_list.filter(
                Q(name__icontains=query)
            ).distinct()
        return queryset_list


class ManageProductAPIView(APIView):
    """ class to manage product model objects"""

    permission_classes = [
        TokenHasReadWriteScope,  # access bearer token
    ]

    @staticmethod
    def get(request):
        """
        Get a product
        :param request: http petition
        :return: serialized product data
        """
        try:
            # get obj
            product = Product.objects.get(pk=request.GET.get('id'))
        except Product.DoesNotExist:
            return Response(json_data(
                status='danger',
                message='Record not found'
            ), status=status.HTTP_204_NO_CONTENT)
        # response with data serialized
        return Response(json_data(
            data=ProductSerializer(instance=product).data
        ), status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        """
        Create product
        :param request: http petition
        :return: product serialized data
        """
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(is_active=True)
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

    @staticmethod
    def put(request):
        """
        Update product
        :param request: http petition
        :return: product serialized data
        """
        try:
            cat = Product.objects.get(pk=request.data['id'])
        except Product.DoesNotExist:
            return Response(json_data(
                message='Record not found',
                status='danger'
            ), status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(json_data(
                data=serializer.data
            ), status=status.HTTP_201_CREATED)
        return Response(json_data(
            message=serializer.errors
        ), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def patch(request):
        """
        Modify product partially according the data to update
        :param request: http petition
        :return: product serialized data
        """
        try:
            product = Product.objects.get(pk=request.data['id'])
        except Product.DoesNotExist:
            return Response(json_data(
                message='Record not found',
                status='danger'
            ), status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(json_data(
                data=serializer.data
            ), status=status.HTTP_201_CREATED)
        return Response(json_data(
            message=serializer.errors
        ), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request):
        """
        delete product
        :param request: http petition
        :return: http response
        """
        data = request.GET
        try:
            product = Product.objects.get(pk=data.get('id'))
        except Product.DoesNotExist:
            return Response(json_data(
                message='Record Not Found',
                status='danger'
            ), status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(json_data(
            message='CONTENT DELETED'
        ), status=status.HTTP_200_OK)
