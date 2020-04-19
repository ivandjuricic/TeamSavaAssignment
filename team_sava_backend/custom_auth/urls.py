from django.urls import path
from rest_framework import routers
from .views import UserViewSet, EmailTokenViewSet, PasswordResetView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.SimpleRouter()
router.register(r'auth-user', UserViewSet)
router.register(r'reset-token', EmailTokenViewSet)

urlpatterns = [
    path('auth-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password/', PasswordResetView.as_view(), name='password-reset'),
]

urlpatterns += router.urls
