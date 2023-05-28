from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'You do not have permission to this selection'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if obj.owner == request.user:
            return True
        if request.user.is_staff:
            return True
        if request.user.role in ['moderator', 'admin']:
            return True
        else:
            return False
