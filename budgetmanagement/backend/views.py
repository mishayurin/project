from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


@api_view(['POST'])
def api_login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        user_profile = UserProfile.objects.get(user=user)
        print(user_profile)
        result = f'success: phone is {user_profile.phone}'
        print(result)
        user_serializer = UserSerializer(user)
        user_profile_serializer = UserProfileSerializer(user_profile)
        result_json = user_profile_serializer.data
        user_json = user_serializer.data
        user_json.pop('password')
        user_json['date_joined'] = user.date_joined.strftime("%Y-%m-%d %H:%M:%S")
        result_json['user'] = user_json
        return Response(result_json)
    else:
        result = 'Unauthorized'
        print(result)
        return Response(result)


@api_view(['POST'])
def api_user_registration(request):
    if request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_profile_serializer = UserProfileSerializer(data=request.data)
            if user_profile_serializer.is_valid():
                user = User.objects.create_user(request.data["username"],
                                                request.data["email"],
                                                request.data["password"])
                user.first_name = request.data["first_name"]
                user.last_name = request.data["last_name"]
                print(user)
                user.save()

                user_profile_dict = {'user': user}
                for field in ['phone', 'photo']:
                    if field in request.data:
                        user_profile_dict[field] = request.data[field]

                user_profile = UserProfile(**user_profile_dict)
                user_profile.save()
                print(user_profile)
                return Response(request.data, status=status.HTTP_201_CREATED)
            else:
                return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
