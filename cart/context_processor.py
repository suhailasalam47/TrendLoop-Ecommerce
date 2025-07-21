from .models import CartItem

def cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_count = sum(cart_items.values_list('quantity', flat=True))

    return {"cart_count": cart_count}