from django.urls import path, include
from rest_framework import routers
from .views import CreateUserView, LoginUserView, ProfileViewSet, PersonalSettingsViewSet, ProjectViewSet, CategoryViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register('profile',ProfileViewSet)
router.register('settings',PersonalSettingsViewSet)
router.register('project',ProjectViewSet)
router.register('category',CategoryViewSet)
router.register('task',TaskViewSet)

urlpatterns = [
    path('user/create/', CreateUserView.as_view(), name='create'),
    path('user/login/', LoginUserView.as_view(), name='login'),
    path('', include(router.urls)),
]
