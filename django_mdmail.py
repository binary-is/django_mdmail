# django_mdmail
# Version: 0.1
# Authors: Helgi Hrafn Gunnarsson <helgi@binary.is>
# Repository: https://github.com/binary-is/django_mdmail
# License: MIT
#
# Description: django_mdmail bridges the gap between the `mdmail` package and
# Django. `mdmail` is a Python module that allows the sending of Markdown
# email. Django is a web development framework which contains its own wrapper
# functions for sending email. This package is a simple wrapper for `mdmail`
# utilizing Django's email settings and imitating Django's email function
# signature. Ideally, a Django user should be able to replace...
#
#     from django.core.mail import send_mail
#
# ...with...
#
#     from django_mdmail import send_mail
#
# ...to send Markdown emails with all the features of `mdmail`.
#
# Installation: This package is a single file with all the necessary
# information provided in comments at the top. To install or upgrade, simply
# place this file wherever you wish, import the `send_mail` function as
# described above and use it according to Django's documentation.
#
# You will need to have these Python packages installed: mdmail django
#
# Limitations:
#
# * Since `mdmail` uses the native Python libraries to send the email,
#   Django's email backend is ignored. The mail gets delivered through SMTP
#   according to Django's email settings, no matter which backend you've
#   chosen.
#
# * The `html_message` parameter does nothing and is provided only for
#   API-compatibility. This is because the HTML is generated from the Markdown
#   provided.
#
# * The `fail_silently` parameter does nothing, because `mdmail` always fails
#   silently.
#
# If you need any of these limitations remedied, please contact the author or
# better yet, contribute fixes and the author will be happy to include them!

from django.conf import settings
import mdmail

def send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None):

    smtp = {
        'host': settings.EMAIL_HOST,
        'port': settings.EMAIL_PORT,
        'tls': settings.EMAIL_USE_TLS,
        'ssl': settings.EMAIL_USE_SSL,
        'user': auth_user or settings.EMAIL_HOST_USER,
        'password': auth_password or settings.EMAIL_HOST_PASSWORD,
    }

    for recipient in recipient_list:
        print(mdmail.send(message, subject, from_email, recipient, smtp=smtp))
