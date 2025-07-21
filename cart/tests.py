from django.test import TestCase, Client
from django.contrib.auth.models import User
from store.models import Product
from .models import Order, OrderItem, CartItem

class OrderFlowTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(product_name='Test Product', price=100, stock=10, description="Test description")

    def test_order_flow(self):
        self.client.login(username='testuser', password='password')
        self.client.post(f'/api/cart/add_cart/{self.product.pk}/', {'stock_value': 2})

        session = self.client.session
        session['total_price'] = {
            'total': 200,
            'sub_total': 180
        }
        session.save()
        
        self.client.post('/api/cart/checkout/', {
            'full_name': 'Suhaila M',
            'address': 'Dubai St',
            'city': 'Dubai',
            'state': 'UAE',
            'phone': '12345678',
        })

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.filter(user=self.user).count(), 0)
