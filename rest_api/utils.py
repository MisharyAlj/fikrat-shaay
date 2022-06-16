from django.contrib.auth import authenticate
from rest_framework import serializers


"""
It takes a nationality_id and password, authenticates the user, and returns the user if the
authentication is successful.
If the authentication fails, it raises a ValidationError 
:param nationality_id: The national ID of the user
:param password: The password to authenticate with
:return: The user object is being returned.
"""


def get_and_authenticate_user(nationality_id, password):
    user = authenticate(nationality_id=nationality_id, password=password)
    if user is None:
        raise serializers.ValidationError(
            "Invalid nationaliy Id/password. Please try again!")
    return user
