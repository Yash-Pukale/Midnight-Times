from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, GetAllUsersView, CustomTokenObtainPairView, MarkUserAsInactiveView

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', GetAllUsersView.as_view(), name='users'),
    path('mark_as_inactive/', MarkUserAsInactiveView.as_view(), name='mark_as_inactive'),
]