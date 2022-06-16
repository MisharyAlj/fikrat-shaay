from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

# The CustomUserManager class inherits from BaseUserManager and overrides the create_user and
# create_superuser methods


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.

    It creates a user with the given email and password.

    :param email: The email address of the user
    :param nationality_id: The id of the nationality of the user
    :param phone: The phone number of the user
    :param password: The password to use for this user
    :return: The user object
    """

    def create_user(self, email, nationality_id, phone, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(
            email=email, nationality_id=nationality_id, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, nationality_id, phone, password,  **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, nationality_id, phone, password,  **extra_fields)
