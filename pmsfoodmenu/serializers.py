from rest_framework import serializers
from .models import Category, Product, Table, Basket, BasketItem


# Category / Product
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


# Table
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ["id", "table_num", "status", "created_at"]


# Basket
class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = [
            "id",
            "product",
            "count",
            "name_az", "name_en", "name_ru",
            "description_az", "description_en", "description_ru",
            "cost",
            "time",
        ]
        read_only_fields = [
            "name_az", "name_en", "name_ru",
            "description_az", "description_en", "description_ru",
            "cost", "time"
        ]


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True)
    table = TableSerializer(read_only=True)
    table_id = serializers.PrimaryKeyRelatedField(
        queryset=Table.objects.all(), source="table", write_only=True
    )

    class Meta:
        model = Basket
        fields = [
            "id",
            "table", "table_id",
            "note", "service_cost", "total_cost", "total_time",
            "items", "created_at"
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        basket = Basket.objects.create(**validated_data)

        total_cost = 0
        total_time = 0

        for item_data in items_data:
            product = item_data["product"]
            count = item_data.get("count", 1)
            BasketItem.objects.create(
                basket=basket,
                product=product,
                count=count
            )
            total_cost += float(product.cost) * count
            total_time += product.time * count

        basket.total_cost = total_cost + float(basket.service_cost)
        basket.total_time = total_time
        basket.save()
        return basket
