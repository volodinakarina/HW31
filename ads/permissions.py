from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'You do not have permission to change this ad'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if obj.author == request.user:
            return True
        if request.user.is_staff:
            return True
        if request.user.role in ['moderator', 'admin']:
            return True
        else:
            return False


class IsModerator(BasePermission):
    message = 'You do not have permission to change this category'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if request.user.role in ['moderator', 'admin']:
            return True
        else:
            return False
