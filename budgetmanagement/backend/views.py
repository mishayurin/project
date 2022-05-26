from .models import UserProfile, Expenses_Types, Limits
from .serializers import UserSerializer, UserProfileSerializer, \
    ExpensesTypesSerializer, LimitsSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
import copy


@api_view(['GET'])
def api_is_authenticated(request):
    if request.user.is_authenticated:
        result_json = {'username': request.user.username}
        return Response(result_json)
    else:
        return Response('Anonymous', status=status.HTTP_401_UNAUTHORIZED)


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

        login(request, user)
        return Response(result_json)
    else:
        result = 'Unauthorized'
        print(result)
        return Response(result, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def api_logout(request):
    if request.user.is_authenticated:
        result = f"User with username: '{request.user.username}' logged out"
        logout(request)
        return Response(result)
    else:
        return Response('Anonymous', status=status.HTTP_401_UNAUTHORIZED)


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


@api_view(['PATCH'])
def api_user(request):
    if request.method == 'PATCH':
        if 'username' not in request.data:
            return Response('''"username": [\
"This field is required."]''', status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated and request.data['username'] == request.user.username:
            user = request.user
            password = None
            user_data = copy.deepcopy(request.data)
            if 'password' in request.data:
                password = user_data.pop('password')
            user_serializer = UserSerializer(user, user_data, partial=True)
            if user_serializer.is_valid():
                user_profile = UserProfile.objects.get(user=user)
                user_profile_serializer = UserProfileSerializer(user_profile,
                                                                data=request.data,
                                                                partial=True)
                if user_profile_serializer.is_valid():
                    if password is not None:
                        try:
                            user.set_password(password)
                        except Exception as e:
                            return Response(e, status=status.HTTP_400_BAD_REQUEST)
                    user_serializer.save()
                    user_profile_serializer.save()
                    return Response(request.data)
                else:
                    return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(f'User with "username" {request.data["username"]} \
is not authorized.', status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_category(request):
    if request.method == 'POST':
        serializer = ExpensesTypesSerializer(data=request.data)
        if serializer.is_valid():
            try:
                expenses_types = serializer.save()
                print(expenses_types.pk)
            except IntegrityError as e:
                error = 'Error: UNIQUE constraint failed: ' \
                        f'{request.data}'
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def api_category_update(request, pk=None):
    if request.method == 'PATCH':
        try:
            expenses_types = Expenses_Types.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ExpensesTypesSerializer(expenses_types, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_limit(request):
    if request.method == 'POST':
        serializer = LimitsSerializer(data=request.data)
        if serializer.is_valid():
            limits = serializer.save()
            print(limits.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def api_limit_update(request, pk=None):
    if request.method == 'PATCH':
        try:
            limits = Limits.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LimitsSerializer(limits, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
