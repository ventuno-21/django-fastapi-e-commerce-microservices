# cart_app/cart.py
import json
import redis
from django.conf import settings
from decimal import Decimal
from .models import Product

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)

# key patterns:
# cart:session:<session_id>  or  cart:user:<user_id>

CART_TTL_SECONDS = 60 * 60 * 24 * 30  # 30 days


class Cart:
    def __init__(self, user_id=None, session_id=None):
        if user_id:
            self.key = f"cart:user:{user_id}"
        elif session_id:
            self.key = f"cart:session:{session_id}"
        else:
            raise ValueError("Provide user_id or session_id")

    def _serialize_item(self, qty, meta=None):
        return json.dumps({"quantity": int(qty), "meta": meta or {}})

    def _deserialize_item(self, s):
        d = json.loads(s)
        d["quantity"] = int(d["quantity"])
        return d

    def add(self, product_id: int, quantity: int = 1, replace_quantity=False):
        pid = str(product_id)
        existing = redis_client.hget(self.key, pid)
        if existing and not replace_quantity:
            data = self._deserialize_item(existing)
            quantity = data["quantity"] + quantity
        redis_client.hset(self.key, pid, self._serialize_item(quantity))
        redis_client.expire(self.key, CART_TTL_SECONDS)

    def set(self, product_id: int, quantity: int):
        redis_client.hset(self.key, str(product_id), self._serialize_item(quantity))
        redis_client.expire(self.key, CART_TTL_SECONDS)

    def remove(self, product_id: int):
        redis_client.hdel(self.key, str(product_id))

    def clear(self):
        redis_client.delete(self.key)

    def items(self):
        raw = redis_client.hgetall(self.key)
        items = []
        ids = [int(k) for k in raw.keys()]
        products = {p.id: p for p in Product.objects.filter(id__in=ids)}
        for k, v in raw.items():
            pid = int(k)
            d = self._deserialize_item(v)
            product = products.get(pid)
            if not product:
                # product removed from DB: skip or remove from cart
                continue
            items.append(
                {
                    "product": product,
                    "quantity": d["quantity"],
                    "meta": d.get("meta", {}),
                    "line_total": product.price * d["quantity"],
                }
            )
        return items

    def total(self):
        total = Decimal("0.00")
        for it in self.items():
            total += it["line_total"]
        return total

    def merge_from(self, other_cart_key):
        """Merge another cart (e.g., session cart) into this cart (user cart)."""
        raw = redis_client.hgetall(other_cart_key)
        for k, v in raw.items():
            my = redis_client.hget(self.key, k)
            if my:
                a = self._deserialize_item(my)["quantity"]
                b = self._deserialize_item(v)["quantity"]
                redis_client.hset(self.key, k, self._serialize_item(a + b))
            else:
                redis_client.hset(self.key, k, v)
        redis_client.expire(self.key, CART_TTL_SECONDS)
        redis_client.delete(other_cart_key)

    def to_order(self, user=None, email=None):
        """
        Create an Order and OrderItems from cart contents.
        IMPORTANT: This function performs DB writes — call inside atomic transaction.
        Returns created Order instance.
        """
        from django.db import transaction
        from cart_app.models import Order, OrderItem

        items = self.items()
        if not items:
            raise ValueError("Cart is empty")

        with transaction.atomic():
            order = Order.objects.create(
                user=user if getattr(user, "is_authenticated", False) else None,
                email=email or (user.email if user else ""),
                total=0,
            )
            total = Decimal("0.00")
            for it in items:
                OrderItem.objects.create(
                    order=order,
                    product=it["product"],
                    quantity=it["quantity"],
                    unit_price=it["product"].price,
                )
                total += it["line_total"]
                # optionally decrement inventory:
                if hasattr(it["product"], "inventory"):
                    it["product"].inventory = max(
                        0, it["product"].inventory - it["quantity"]
                    )
                    it["product"].save(update_fields=["inventory"])
            order.total = total
            order.save(update_fields=["total"])
            # clear cart after checkout
            self.clear()
            return order
