from django.urls import path, include
from rest_framework import routers
from .views import CreateUserView, LoginUserView, ProfileViewSet, ProfileViewSet, PersonalSettingViewSet, \
    ProjectViewSet, CategoryViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register('user/profile', ProfileViewSet)
router.register('user/setting', PersonalSettingViewSet)
router.register('profile', ProfileViewSet)
router.register('project', ProjectViewSet)
router.register('category', CategoryViewSet)
router.register('task', TaskViewSet)

urlpatterns = [
    path('user/create/', CreateUserView.as_view(), name='create'),
    path('user/login/', LoginUserView.as_view(), name='login'),
    # path('profile/', LoginUserProfileView.as_view(), name='profile'),
    # path('user/update/', UpdateUserView.as_view(), name='update'),
    path('', include(router.urls)),
]
