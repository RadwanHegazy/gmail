from django.urls import path
from .views import (
    profile,
    register
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/profile/', profile.ProfileAPIView.as_view(), name="profile"),
    path('v1/register/', register.RegisterAPIView.as_view(), name="register"),

]
