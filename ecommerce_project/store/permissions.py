from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, req, view):
        return req.user.role == 'admin'

class IsVendor(permissions.BasePermission):
    def has_permission(self, req, view):
        return req.user.role == 'vendor'

class IsCustomer(permissions.BasePermission):
    def has_permission(self, req, view):
        return req.user.role == 'customer'
