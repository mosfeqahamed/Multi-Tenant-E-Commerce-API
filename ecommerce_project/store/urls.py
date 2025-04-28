from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, JWTLoginView, JWTRefreshView,
    VendorViewSet, ProductViewSet, OrderViewSet
)

router = DefaultRouter()
router.register(r'auth',    RegisterView,   basename='auth')
router.register(r'vendors', VendorViewSet,  basename='vendor')
router.register(r'products',ProductViewSet, basename='product')
router.register(r'orders',  OrderViewSet,   basename='order')

urlpatterns = [
    path('token/',         JWTLoginView.as_view(),   name='token_obtain_pair'),
    path('token/refresh/', JWTRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
