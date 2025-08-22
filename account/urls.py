from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.UserLoginView.as_view(), name='login'),
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('verify', views.VerificationCodeView.as_view(), name='verify'),
    path('profile', views.UserProfileView.as_view(), name='profile'),
    path('profile/update', views.UserProfileUpdatedView.as_view(), name='profile_update'),

]