from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter

from .serializers import BaseUserSerializer, BaseUserPublicSerializer
from .permissions import IsAdminOrRestrictedAccess

User = get_user_model()

class BaseUserViewSet(ModelViewSet):
    queryset = User.objects.all().exclude(is_staff=True)
    serializer_class = BaseUserSerializer
    authentication_classes = [TokenAuthentication]
    filter_backends = [OrderingFilter]
    ordering = ["id"]
    permission_classes = [IsAdminOrRestrictedAccess]

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return self.queryset.filter(username=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ["POST","PUT", "PATCH",]:
            return BaseUserPublicSerializer
        return super().get_serializer_class()

# Create your views here.
