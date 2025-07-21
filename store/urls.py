from django.urls import path
from .views import store, product_detail, ProductViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')


urlpatterns = [
    path('', store, name='store'),
    path('product_detail/<int:pk>/', product_detail, name='product_detail'),
] + router.urls