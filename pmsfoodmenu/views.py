from rest_framework import viewsets
from .models import Category, Product, Table, Basket
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    TableSerializer,
    BasketSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by("table_num")
    serializer_class = TableSerializer


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all().order_by("-created_at")
    serializer_class = BasketSerializer
