# cart_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    OrderViewSet,
    CategoryViewSet,
    add_to_cart,
    get_cart,
    remove_from_cart,
    checkout_cart,
)

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"category", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
    path("cart/add/", add_to_cart),
    path("cart/", get_cart),
    path("cart/remove/", remove_from_cart),
    path("cart/checkout/", checkout_cart),
]
