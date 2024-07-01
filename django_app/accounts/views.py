# write register view
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime
from utils.api_response import api_success_response
from .serializers import UserSerializer
from .models import CustomUser
    

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    def post(self, request):
        """
        Handles the HTTP POST request to create a new user.

        Args:
            request (rest_framework.request.Request): The HTTP request object.

        Returns:
            rest_framework.response.Response: The HTTP response containing the serialized user data if the user is created successfully.
            rest_framework.response.Response: The HTTP response containing the serialized validation errors if the user data is invalid.
        """
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = CustomUser.objects.get(email=data['email'])
            user_data = UserSerializer(user).data
        else:
            return api_success_response(serializer.errors)
        return api_success_response(user_data)
    

class GetAllUsersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """
        Handles the HTTP GET request to retrieve all users.

        Args:
            request (rest_framework.request.Request): The HTTP request object.

        Returns:
            rest_framework.response.Response: The HTTP response containing the serialized data of all users.
        """
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        user_data = serializer.data
        for user in user_data:
            user['password'] = ''
            datdate_joined = datetime.strptime(user['date_joined'], "%Y-%m-%dT%H:%M:%S.%fZ")
            user['date_joined'] = datdate_joined.strftime("%B %d, %Y %H:%M:%S")
        return api_success_response(user_data)
    

class MarkUserAsInactiveView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def post(self, request):
        """
        Handles the HTTP POST request to mark a user as inactive.

        Args:
            request (rest_framework.request.Request): The HTTP request object.

        Returns:
            rest_framework.response.Response: The HTTP response containing the serialized data of the marked user.
        """
        data = request.data
        user = CustomUser.objects.get(email=data['email'])
        user.is_active = data['is_active']
        user.save()
        user_data = UserSerializer(user).data
        return api_success_response(user_data)
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
        """
        Get a token for the given user.

        Args:
            cls (Type[CustomTokenObtainPairSerializer]): The class of the serializer.
            user (CustomUser): The user for whom the token is being generated.

        Returns:
            Token: The generated token.
        """
        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)

            return token
    
        def validate(self, attrs):
            data = super().validate(attrs)
    
            user = self.user
            data["user_id"] = user.id
            data["is_admin"] = user.is_superuser
            # ... add other user information as needed
    
            return data
    
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer