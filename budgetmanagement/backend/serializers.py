from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, Expenses_Types
from django.db import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone', 'photo')


class ExpensesTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses_Types
        fields = ('Category', 'Name_of_expenses_types')
