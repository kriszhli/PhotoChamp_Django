from rest_framework.routers import DefaultRouter
from .views import ChallengeViewSet, EntryViewSet

router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet)
router.register(r'entries',    EntryViewSet)

urlpatterns = router.urls
