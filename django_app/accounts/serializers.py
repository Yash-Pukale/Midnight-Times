# create user
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        """
        Create a new user using the validated data.

        Parameters:
            validated_data (dict): A dictionary containing the validated data for creating a user.

        Returns:
            User
        """
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = '__all__'