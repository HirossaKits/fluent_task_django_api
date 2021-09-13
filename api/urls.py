from django.urls import path, include
from rest_framework import routers
from .views import CreateUserView, LoginUserView, ProfileViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register('profile',ProfileViewSet)
router.register('task',TaskViewSet)
# router.register('category',)

urlpatterns = [
    path('user/create/', CreateUserView.as_view(), name='create'),
    path('user/login/', LoginUserView.as_view(), name='login'),
    path('', include(router.urls)),
]
