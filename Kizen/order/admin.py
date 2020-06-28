from django.contrib import admin
from order.models.order import Order, OrderLine


admin.site.register(Order)
admin.site.register(OrderLine)
