from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomBackend(ModelBackend):
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticates a user based on the provided email and password.

        Args:
            request (HttpRequest): The HTTP request object.
            email (str): The email of the user to authenticate.
            password (str): The password of the user to authenticate.
            **kwargs: Additional keyword arguments.

        Returns:
            User
        """
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def user_can_authenticate(self, user):
        """
        Check if the user is active.

        Args:
            user (User): The user object.

        Returns:
            bool: True if the user is active, False otherwise.
        """
        return user.is_active
