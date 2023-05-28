from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from selections.models import Selection
from selections.permissions import IsOwner
from selections.serializers import SelectionListSerializer, SelectionDetailSerializer, SelectionCreateSerializer, \
    SelectionUpdateSerializer


class SelectionGenericViewSet(viewsets.GenericViewSet):
    queryset = Selection.objects.filter(is_active=True).prefetch_related('items').select_related('owner').all()
    serializers = {
        "list": SelectionListSerializer,
        "retrieve": SelectionDetailSerializer,
        "create": SelectionCreateSerializer,
        'update': SelectionUpdateSerializer,
        'partial_update': SelectionUpdateSerializer,
    }
    default_serializer = SelectionListSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAuthenticated()]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsOwner()]
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def retrieve(self, request, pk):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=200)

    def create(self, request):
        data = request.data
        data['owner_id'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def update(self, request, pk):
        selection = self.get_object()
        serializer = self.get_serializer(selection, data=request.data)
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
        item = self.get_object()
        item.is_active = False
        item.save()
        return Response({'status': 'ok'}, status=204)
