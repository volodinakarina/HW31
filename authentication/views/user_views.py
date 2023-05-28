from django.db.models import Count, Q
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from authentication.permission import IsUser
from authentication.serializers.user_serializer import UserListSerializer, \
    UserRetrieveSerializer, UserChangePasswordSerializer, UserUpdateSerializer, UserCreateSerializer


class UsersGenericViewSet(viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True).prefetch_related('locations').annotate(
        total_ads=Count('ad', filter=Q(ad__is_published=True))).order_by('username').all()
    serializers = {
        "list": UserListSerializer,
        "retrieve": UserRetrieveSerializer,
        'update': UserUpdateSerializer,
        'partial_update': UserUpdateSerializer,
    }
    default_serializer = UserListSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsUser()]
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def retrieve(self, request, pk):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=200)

    def update(self, request, pk):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk):
        user = self.get_object()
        data = request.data
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def destroy(self, request, pk):
        item: User = self.get_object()
        item.is_active = False
        item.save()
        return Response({'status': 'ok'}, status=204)


class UserCreateView(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer


class UserChangePasswordView(APIView):
    model = User
    serializer_class = UserChangePasswordSerializer
    permission_classes = IsAuthenticated

    def post(self, request):
        user = request.user
        data = request.data
        serializer = self.serializer_class(instance=user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({'status': 'ok'}, status=200)
