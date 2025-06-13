from rest_framework.generics import ListAPIView
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.viewsets import ModelViewSet
from apps.users.models import User
from apps.users.serializers import UserSerializer


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.filter(parent=None).prefetch_related('subcategories')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.prefetch_related('colors__images')
    serializer_class = ProductSerializer


class ProductDetailView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
