from django.urls import path
from .views import UserRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login' ),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh' ),
    path('logout/', TokenBlacklistView.as_view(), name='logout' )
]