from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrRestrictedAccess(BasePermission):
    def has_permission(self, request, view):
        # Allow all authenticated users to access the view
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow read-only access to all authenticated users
        if request.method in SAFE_METHODS:
            return True

        # Allow staff members to access all methods
        if request.user.is_staff:
            return True

        # Allow non-staff users to access retrieve, update, and delete methods
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            return obj.username == request.user.username

        return False
