from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/profile/', ProfileView.as_view(template_name='profile.html'), name='profile'),
    path('profile/<int:pk>/', ProfileDetail.as_view(), name='profile_detail'),
    path('profile/<int:pk>/edit/', ProfileUpdate.as_view(), name='profile_edit'),
    path('profile/<int:pk>/delete/', ProfileDelete.as_view(), name='profile_delete'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('author_now/', author_now, name='author_now'),
]
