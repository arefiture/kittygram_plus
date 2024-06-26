from django.urls import include, path

from rest_framework.routers import DefaultRouter

from cats.views import AchievementViewSet, CatViewSet, OwnerViewSet


router = DefaultRouter()
router.register('cats', CatViewSet)
router.register('owners', OwnerViewSet)
router.register('achievements', AchievementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
