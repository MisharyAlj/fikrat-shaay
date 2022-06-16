from rest_framework import permissions

"""
If the request is a safe method (GET, HEAD, OPTIONS), then return True. Otherwise, return True 
if the user is a superuser
    
:param request: The incoming request
:param view: The view that we're checking permissions against
"""


class IsSuperuserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        is_superuser = request.user and request.user.is_superuser
        return is_superuser


"""
If the user is a superuser, then they have permission to do whatever they want
    
:param request: The incoming request
:param view: The view that we're checking permissions against
:return: The is_superuser variable is being returned.
"""


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Write permissions are only allowed to the owner of the snippet.
        is_superuser = request.user and request.user.is_superuser
        return is_superuser
