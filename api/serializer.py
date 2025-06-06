from rest_framework import serializers
from .models import Product , Order , OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "stock",
            "image"
        ]
    
    # Validate that the price is greater than 0
    def validate_stock(self , value):
        if value <= 0:
            raise serializers.ValidationError(
                "Stock must be greater than 0."
            )
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source = "product.name")
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source = "product.price")
    class Meta:
        model = OrderItem
        fields = [
            "product_name" ,
            "product_price",
            "quantity",
            "item_subtotal"
            ]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True , read_only=True)
    total_price = serializers.SerializerMethodField(method_name="total")

    def total(self, obj):
        items = obj.items.all()
        return sum(item.item_subtotal for item in items)
    
    class Meta:
        model = Order
        fields = [
            "order_id",
            "user",
            "created_at",
            "status",
            "items",
            "total_price"
        ]

class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()

