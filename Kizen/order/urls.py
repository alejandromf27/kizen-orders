from django.conf.urls import url
from order.views.v1 import order

urlpatterns = [
    url(r'manage/', order.ManageOrderAPIView.as_view(), name="manage orders"),
    url(r'list/', order.ApiOrdersListView.as_view(), name="paginate list of orders"),
    url(r'products/', order.ApiOrdersProductsListView.as_view(), name="product orders query"),
]
