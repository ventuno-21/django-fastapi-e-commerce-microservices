# cart_app/serializers.py
from rest_framework import serializers
from .models import Product, Category, Order, OrderItem
from utils.logger import logger


class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source="parent.name", read_only=True)
    parnt_id_name = serializers.SerializerMethodField()

    def get_parnt_id_name(self, obj):

        if obj.parent:
            result = f"parnet id : {obj.parent.id} , parnet name: {obj.parent.name} "
            return result

        result = f"No parent id or name "
        return result

    class Meta:
        model = Category
        fields = ["id", "slug", "name", "parent", "parent_name", "parnt_id_name"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Category.objects.all(),
        source="category",
        required=False,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "sku",
            "name",
            "description",
            "price",
            "inventory",
            "is_active",
            "category",
            "category_id",
            "created_at",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Product.objects.all(), source="product"
    )

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_id", "quantity", "unit_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user_id", "email", "total", "status", "created_at", "items"]
        read_only_fields = ["total", "status", "created_at", "user_id"]
