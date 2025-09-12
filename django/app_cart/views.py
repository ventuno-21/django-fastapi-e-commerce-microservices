# cart_app/views.py
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from utils.logger import logger

from django.conf import settings
from django.shortcuts import get_object_or_404

from .cart import Cart
from .models import Category, Order, Product
from .serializers import CategorySerializer, OrderSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        logger.debug(
            f"inside the create method of ProductViewset & user is is: {request.user.id}"
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter()
    serializer_class = CategorySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    # optionally require auth for create/list
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create order manually with items in the payload.
        (Alternately, use cart checkout endpoint below)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # create order and items
        order = serializer.save()
        return Response(self.get_serializer(order).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])  # allow both guest and authenticated users
def add_to_cart(request):
    """
    Body: { "product_id": 1, "quantity": 2 }
    - If user is authenticated (JWT), use user-based cart
    - If user is a guest, use session-based cart
    """
    data = request.data
    pid = data.get("product_id")
    qty = int(data.get("quantity", 1))

    # Determine whether user is authenticated via JWT
    if hasattr(request, "user") and getattr(request.user, "is_authenticated", False):
        # Authenticated user → cart keyed by user_id
        cart = Cart(user_id=request.user.id)
    else:
        # Guest user → cart keyed by session_id
        if not request.session.session_key:
            request.session.create()  # create new session if not exists
        cart = Cart(session_id=request.session.session_key)

    # Add product to cart
    cart.add(pid, qty)

    # Return number of items in cart
    return Response(
        {
            "status": "ok",
            "cart_items": len(cart.items()),
        }
    )


@api_view(["GET"])
def get_cart(request):
    if request.user.is_authenticated:
        cart = Cart(user_id=request.user.id)
    else:
        if not request.session.session_key:
            request.session.create()
        cart = Cart(session_id=request.session.session_key)
    items = []
    for it in cart.items():
        items.append(
            {
                "product_id": it["product"].id,
                "name": it["product"].name,
                "quantity": it["quantity"],
                "unit_price": str(it["product"].price),
                "line_total": str(it["line_total"]),
            }
        )
    return Response({"items": items, "total": str(cart.total())})


@api_view(["POST"])
def remove_from_cart(request):
    pid = request.data.get("product_id")
    if request.user.is_authenticated:
        cart = Cart(user_id=request.user.id)
    else:
        if not request.session.session_key:
            request.session.create()
        cart = Cart(session_id=request.session.session_key)
    cart.remove(pid)
    return Response({"status": "ok"})


@api_view(["POST"])
def checkout_cart(request):
    """
    Checkout: create Order from cart. If user authenticated use user, else require email in body.
    """
    if request.user.is_authenticated:
        cart = Cart(user_id=request.user.id)
        email = request.user.email
        user = request.user
    else:
        if not request.session.session_key:
            return Response({"detail": "No session/cart"}, status=400)
        cart = Cart(session_id=request.session.session_key)
        email = request.data.get("email")
        user = None
        if not email:
            return Response({"detail": "email required for guest checkout"}, status=400)
    try:
        order = cart.to_order(user=user, email=email)
    except Exception as e:
        return Response({"detail": str(e)}, status=400)
    return Response({"order_id": order.id, "total": str(order.total)})
