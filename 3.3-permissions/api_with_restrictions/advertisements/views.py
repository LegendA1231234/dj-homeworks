from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.filters import AdvertisementFilter


class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all().order_by('-created_at')
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAuthenticated()]
        return []

    def perform_destroy(self, instance):
        if instance.creator != self.request.user:
            raise PermissionDenied("Удалять можно только свои объявления")
        instance.delete()

    def perform_update(self, serializer):
        if serializer.instance.creator != self.request.user:
            raise PermissionDenied("Редактировать можно только свои объявления")
        serializer.save()
