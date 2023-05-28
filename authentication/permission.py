from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    message = 'You do not have permission to change this user'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if obj == request.user:
            return True
        if request.user.is_staff:
            return True
        if request.user.role in ['moderator', 'admin']:
            return True
        else:
            return False
