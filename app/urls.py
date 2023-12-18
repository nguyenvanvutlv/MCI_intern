# accounts/urls.py

from django.urls import path
from app.views import UserRegister, UserLogout, ProjectAPI
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('project/', ProjectAPI.as_view(), name='project'),
]