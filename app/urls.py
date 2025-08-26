from rest_framework.routers import DefaultRouter
from .views import PageViewSet

app_name = 'api'

router = DefaultRouter()
router.register('pages', PageViewSet, basename='page')

urlpatterns = router.urls