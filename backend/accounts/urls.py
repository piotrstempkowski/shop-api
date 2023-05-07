from rest_framework.routers import SimpleRouter
from .views import BaseUserViewSet

router = SimpleRouter()
router.register(r"user", BaseUserViewSet, basename="user")

urlpatterns = router.urls