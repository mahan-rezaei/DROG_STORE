from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_token
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('user_list/', views.UserListView.as_view(), name='user_list'),
    path('api-token-auth/', auth_token.obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]





# "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNDg5MTM4MCwiaWF0IjoxNzM0ODA0OTgwLCJqdGkiOiJiNzBhY2U0NGZjMzA0ZjBmODU1ZmE2Y2IwMWI4YWNlNiIsInVzZXJfaWQiOjF9.LEXJw9ysJmuwSlno4X2PCiG8IhjCsRK72XET14m-ZUo",
# "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0ODA1MjgwLCJpYXQiOjE3MzQ4MDQ5ODAsImp0aSI6ImZmMTY1MTE3MzRhYjRkZjhiZTcwNDZiNjVjYTk5Mzc5IiwidXNlcl9pZCI6MX0.lnbF6ngCdFkuvTgGHc_S9vh2jO30GIX0_3b2yGT44bY"