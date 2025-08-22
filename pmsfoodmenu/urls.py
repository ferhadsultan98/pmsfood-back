from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, TableViewSet, BasketViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)

router.register(r'tables', TableViewSet)
router.register(r'baskets', BasketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]




