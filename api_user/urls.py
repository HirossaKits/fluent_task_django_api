from django.urls import path, include
from rest_framework import routers
from .views import CreateUserView, LoginUserView, UpdateUserView

router = routers.DefaultRouter()
# router.register('category',)

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('', include(router.urls)),
]
