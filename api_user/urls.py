from django.urls import path, include
from rest_framework import routers
from .views import CreateUserView, LoginUserView, ProfileViewSet,

router = routers.DefaultRouter()
router.register('profile',ProfileViewSet)
# router.register('category',)

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile',ProfileViewSet.as_view(), name='profile'),
    # path('profile/', ProfileViewSet.as_view(), name='profile'),
    path('', include(router.urls)),
]
