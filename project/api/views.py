from django.http import JsonResponse
from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Product , Order , OrderItem
from .serializer import ProductSerializer , OrderSerializer , ProductInfoSerializer
from dataclasses import dataclass

@api_view(["GET"])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products , many = True)
    return Response(serializer.data)

@api_view(["GET"])
def product_details(request,pk):
    product = get_object_or_404(Product , pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def order_list(request):
    orders = Order.objects.prefetch_related("items","items__product")
    serializer = OrderSerializer(orders , many=True)
    return Response(serializer.data)

@api_view(["GET"])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        "products":products,
        "count":len(products),
        "max_price": products.aggregate(max_price=Max("price"))["max_price"]
    })
    return Response(serializer.data)

