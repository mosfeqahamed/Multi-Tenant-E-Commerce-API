from rest_framework import viewsets, mixins,  permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models       import User, Vendor, Product, Order
from .serializers  import (
    UserSerializer, VendorSerializer,
    ProductSerializer, OrderSerializer
)
from store.permissions  import IsAdmin, IsVendor, IsCustomer

# -- Auth & Registration --

class RegisterView(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response({'id': user.id, 'username':user.username})

class JWTLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

class JWTRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

# -- Vendor (read-only) --

class VendorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

# -- Product (CRUD) --

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'vendor':
            return Product.objects.filter(vendor__user=user)
        return Product.objects.all()

    def perform_create(self, serializer):
        vid = self.request.user.vendor.id
        serializer.save(vendor_id=vid)

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsVendor() | IsAdmin()]
        return [permissions.IsAuthenticated()]

# -- Order (customers create, others view) --

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Order.objects.filter(customer=user)
        if user.role == 'vendor':
            return Order.objects.filter(products__vendor__user=user).distinct()
        return Order.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsCustomer()]
        return [permissions.IsAuthenticated()]
