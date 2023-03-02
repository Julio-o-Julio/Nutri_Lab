import re
from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User

def username_is_valid (request, username):
    
    if username_is_empty(request, username):
        return False

    if len(username) < 2:
        messages.add_message(request, constants.ERROR, 'Seu nome de usuário deve conter pelo menos 2 caracteres!')
        return False

    if re.search(r'\s', username):
        messages.add_message(request, constants.ERROR, 'Seu nome de usuário não deve conter espaços!')
        return False

    if User.objects.filter(username=username).first():
        messages.add_message(request, constants.ERROR, 'Nome de usuário já existente!')
        return False

    return True

def email_is_valid (request, email):
    if len(email) == 0:
        messages.add_message(request, constants.ERROR, 'Escreva seu email para prosseguir!')
        return False

    if re.search(r'^[\w-]+@ [a-z\d]+\.[\w]{3}', email):
        messages.add_message(request, constants.ERROR, 'Email invalido!')
        return False

    return True

def password_is_valid (request, password, confirm_password):

    if password_is_empty(request, password):
        return False

    if len(password) < 8:
        messages.add_message(request, constants.ERROR, 'Sua senha deve conter 8 ou mais caractertes')
        return False

    if not password == confirm_password:
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem!')
        return False

    if not re.search('[A-Z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras maiúsculas')
        return False

    if not re.search('[a-z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contem letras minúsculas')
        return False

    if not re.search('[1-9]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contém números')
        return False

    return True

def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:

    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)

    email.attach_alternative(html_content, 'text/html')
    email.send()

    return {'status': 1}

def username_is_empty (request, username):

    if len(username) == 0:
        messages.add_message(request, constants.ERROR, 'Escreva seu nome de usuário para prosseguir!')
        return True
    
    return False

def password_is_empty(request, password):

    if len(password) == 0:
        messages.add_message(request, constants.ERROR, 'Escreva sua senha para prosseguir!')
        return True

    return False