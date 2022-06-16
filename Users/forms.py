from django import forms
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class Sign_inForm(forms.Form):
    national_id = forms.CharField(
        label=_('National ID or email'), max_length=100)
    password = forms.CharField(
        label=_('Password'), max_length=100, widget=forms.PasswordInput())
    remember_me = forms.BooleanField(
        label=_('Remember me'), required=False)


class NewUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'nationality_id', 'phone', 'email', 'occupation',
                  'salary', 'is_superuser', 'is_staff', 'is_active', 'user_permissions', 'password']
