from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django import template
from core.settings.base import EMAIL_HOST_USER


"""
It sends an email to the user with a link to reset their password
    
:param sender: The sender of the email
:param instance: The User instance that requested the password reset
:param reset_password_token: The token object that was just created
:return: the email message.
"""


''' @receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    email_plaintext_message = "{}?token={}".format(
        reverse('password_reset:reset-password-request'), reset_password_token.key)
    # send an e-mail to the user
    subject = "[Fikrat Shaay] Please reset your password"
    plaintext = template.loader.get_template(
        'password/password_reset_email.txt')
    htmltemplate = template.loader.get_template(
        'password/password_reset_email.html')
    c = {
        'email': reset_password_token.user.email,
        'domain': '127.0.0.1:8000',
        'site_name': 'Fikrat Shaay',
        'uid': urlsafe_base64_encode(force_bytes(reset_password_token.user.pk)),
        'user': reset_password_token.user,
        'token': reset_password_token.key,
        'protocol': 'http',
    }
    text_content = plaintext.render(c)
    html_content = htmltemplate.render(c)
    try:
        msg = EmailMultiAlternatives(subject, text_content, 'Fikrat Shaay <{EMAIL_HOST_USER}>', [
            reset_password_token.user.email], headers={'Replay-to': EMAIL_HOST_USER})
        msg.attach_alternative(email_plaintext_message, 'text/html')
        msg.send()
    except BadHeaderError:
        return
 '''
