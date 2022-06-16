
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.contrib.auth import login, logout, authenticate
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import redirect, render
from django import template
from django.http import HttpResponse
from django.contrib import messages
from .models import CustomUser
from core.settings.base import EMAIL_HOST_USER
from . import forms

from django.utils.translation import gettext

"""
If the user is already authenticated, redirect them to the dashboard. 
Otherwise, render the login page with the form.
if the request method is POST, authenticate the user with the provided credentials and
redirect them to the dashboard if they are authenticated, otherwise redirect them to the login page
with an error message.

:param request: The current request object
:return: a render object.
"""


def Login(request):

    if request.method == 'POST':
        form = forms.Sign_inForm(request.POST)
        if form.is_valid():
            national_id = form.cleaned_data['national_id']
            password = form.cleaned_data['password']
            #remember_me = form.cleaned_data['remember_me']
            user = authenticate(
                request, nationality_id=national_id, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, gettext(
                'Your loged in seccsesfully.'))
            if not form.cleaned_data.get('remember_me'):
                # <-- Here if the remember me is False, that is why expiry is set to 0 seconds. So it will automatically close the session after the browser is closed.
                request.session.set_expiry(0)
            return redirect('dashboard')
        else:
            messages.error(
                request, gettext('Incorrect national ID/email or password.'))
            return redirect('login')
    else:
        form = forms.Sign_inForm()
    context = {
        'title': gettext('Backoffice sign in'),
        'form': form,
    }
    return render(request, 'Users/sign_in.html', context)


"""
It logs out the user and redirects to the login page

:param request: The request is a HttpRequest object
:return: The redirect function.
"""


def Logout(request):
    logout(request)
    messages.success(request, gettext('You are logedout succssessuly.'))
    return redirect('login')


"""
If the request method is POST, then create a password reset form with the request data, if the form
is valid, then get the email data from the form, then get the associated users with the email data,
if the associated users exist, then for each user, create a subject, plaintext, html template, and
context, then render the plaintext and html template with the context, then send the email, then
redirect to the password reset done page, otherwise, create a password reset form, then render the
password reset page with the password reset form and title
    
:param request: The request object
:return: a render object.
"""


def password_reset_request(request):
    # It's a function that takes a request object, then if the request
    # method is POST, then create a password reset form with the
    # request data, if the form is valid, then get the email data from
    # the form, then get the associated users with the email data, if
    # the associated users exist, then for each user, create a
    # subject, plaintext, html template, and context, then render the
    # plaintext and html template with the context, then send the
    # email, then redirect to the password reset done page, otherwise,
    # create a password reset form, then render the password reset
    # page with the password reset form and title
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(
                Q(email=data) | Q(nationality_id=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "[Fikrat Shaay] Please reset your password"
                    plaintext = template.loader.get_template(
                        'password/password_reset_email.txt')
                    htmltemplate = template.loader.get_template(
                        'password/password_reset_email.html')
                    c = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Fikrat Shaay',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    text_content = plaintext.render(c)
                    html_content = htmltemplate.render(c)
                    try:
                        msg = EmailMultiAlternatives(subject, text_content, 'Fikrat Shaay <{EMAIL_HOST_USER}>', [
                                                     user.email], headers={'Replay-to': EMAIL_HOST_USER})
                        msg.attach_alternative(html_content, 'text/html')
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.info(
                        request, 'password reset instructions have been sent to the email address entered.')
                    return redirect('/user/password_reset/done/')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name='password/password_reset.html', context={"password_reset_form": password_reset_form, 'title': 'Reset your password'})
