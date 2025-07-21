from django.shortcuts import render, get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer = ProductSerializer
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


def store(request):
    products = Product.objects.all()
    count = products.count()
    context = {
        'products': products,
        'count': count
    }
    return render(request, 'store.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        "product": product
    }
    return render(request, 'product_detail.html', context)

