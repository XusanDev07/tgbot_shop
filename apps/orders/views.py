from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAdminUser

from .models import Basket, OrderItem, Order
from .serializers import BasketSerializer, OrderSerializer


class BasketListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BasketSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BasketDeleteAPIView(generics.DestroyAPIView):
    queryset = Basket.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)

        baskets = Basket.objects.filter(user=self.request.user)
        for item in baskets:
            OrderItem.objects.create(
                order=order,
                product=item.color.product,
                color=item.color,
                quantity=item.quantity
            )
        baskets.delete()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
