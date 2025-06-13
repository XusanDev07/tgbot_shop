from django.urls import path
from .views import BasketListCreateAPIView, BasketDeleteAPIView, OrderListCreateAPIView

urlpatterns = [
    path('basket/', BasketListCreateAPIView.as_view(), name='basket-list-create'),
    path('basket/<int:pk>/', BasketDeleteAPIView.as_view(), name='basket-delete'),

    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
]
