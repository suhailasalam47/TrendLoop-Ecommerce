from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product
from .models import *
from django.contrib import messages
from rest_framework import viewsets, permissions
from .serializers import OrderSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@login_required
def cart(request):
    sub_total, tax, total = 0, 0, 0
    cart_items = CartItem.objects.filter(user=request.user)
    for i in cart_items:
        sub_total += i.sub_total()
    tax = sub_total * 0.02
    total = sub_total + tax
    request.session["total_price"] = {
        "sub_total" : sub_total,
        "total" : total
    }
    context = {
        "cart_items" : cart_items,
        "sub_total" : sub_total,
        "tax" : round(tax, 2),
        "total" : total
    }
    return render(request, 'cart.html', context)


@login_required
def add_cart(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        stock = request.POST.get('stock_value')
        print("stock ====", stock)
        cart_item, created = CartItem.objects.get_or_create(
            user = request.user,
            product = product
            )
        if int(stock) > cart_item.product.stock:
            messages.warning(request, f"Only {cart_item.product.stock} item available.")
            return redirect('product_detail', pk=pk)
        else:
            cart_item.quantity += int(stock)
            print("cart_item.quantity", cart_item.quantity)
            cart_item.save()
        return redirect('cart')
    

def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    action = request.POST.get('action')
    stock = cart_item.product.stock

    if action == 'increase':
        if cart_item.quantity + 1 > stock:
            messages.warning(request, f"Only {stock} items available in stock.")
        else:
            cart_item.quantity += 1
            cart_item.save()

    elif action == 'decrease':
        if cart_item.quantity > 1:
            print("yess")
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart')


def remove_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.warning(request, "Your cart is empty!")
        return redirect('cart')
    total_price = request.session.get('total_price')
    
    total = total_price["total"]
    sub_total = total_price['sub_total']

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone = request.POST.get('phone')

        order = Order.objects.create(
                user= request.user,
                full_name = full_name,
                address = address,
                city = city,
                state = state,
                phone = phone,
                total = total
            )
        order.save()
        for item in cart_items:
            OrderItem.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()

        #Clear cart items
        cart_items.delete()
        return redirect('place_order')
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'sub_total': sub_total
    }
    return render(request, 'checkout.html', context)


def place_order(request):
    return render(request, 'orders.html')