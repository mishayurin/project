from django.urls import path
from .views import api_user_registration, api_login

urlpatterns = [
	path('api/auth/login', api_login),
	path('api/auth/registration', api_user_registration)
]