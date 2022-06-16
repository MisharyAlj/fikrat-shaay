from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# The CustomUser class inherits from AbstractUser and overrides the username field with None.
# The email field is required.
# The USERNAME_FIELD is set to nationality_id.
# The REQUIRED_FIELDS are set to phone and email


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(unique=True, max_length=13)
    nationality_id = models.CharField(
        _('National ID'), unique=True, max_length=10)
    occupation = models.CharField(_('Occupation'), max_length=100)
    salary = models.DecimalField(_('Salary'),
                                 max_digits=6, decimal_places=2, blank=True, null=True)

    USERNAME_FIELD = 'nationality_id'
    REQUIRED_FIELDS = ['phone', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
