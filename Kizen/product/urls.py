from django.conf.urls import url
from product.views.v1 import product

urlpatterns = [
    url(r'manage/', product.ManageProductAPIView.as_view(), name="manage products"),
    url(r'list/', product.ApiProductsListView.as_view(), name="paginate list of products"),
]
