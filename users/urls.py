from django.urls import path
from .views import UserDetailView, ProfileDetailView, UserRegisterView,ProfileUpdateView,CustomTokenObtainPairView, StudentListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('students/', StudentListView.as_view(), name='student-list'),
]