from django.shortcuts import render
from store.models import *

def home(request):
    products = Product.objects.all()[0:8]
    context = {
        'products': products
    }
    return render(request, 'index.html', context)