from django.urls import path
from .views import api_user_registration, api_login, api_logout, api_is_authenticated, \
	api_user

urlpatterns = [
	path('api/auth/login', api_login),
	path('api/auth/logout', api_logout),
	path('api/auth/registration', api_user_registration),
	path('api/auth/is_authenticated', api_is_authenticated),
	path('api/user', api_user),
]