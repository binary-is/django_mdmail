# django_mdmail
# Version: 0.2
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
# Note: The parameter `html_message` can be used to override the HTML
# generated from Markdown but this feature should only be used under special
# circumstances because it defies the whole point of using `django_mdmail` in
# the first place.

from django.core.mail import EmailMultiAlternatives
from email.MIMEImage import MIMEImage
from mdmail import EmailContent

def send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None):

    # Have `mdmail` do its Markdown magic.
    content = EmailContent(message)

    # Create the email message and fill it with the relevant data.
    email = EmailMultiAlternatives(
        subject,
        content.text,
        from_email,
        recipient_list
    )
    email.attach_alternative(html_message or content.html, 'text/html')
    email.mixed_subtype = 'related'

    for filename, data in content.inline_images:
        # Create the image from the image data.
        image = MIMEImage(data.read())

        # Give the image an ID so that it can be found via HTML.
        image.add_header('Content-ID', '<{}>'.format(filename))

        # This header allows users of some email clients (for example
        # Thunderbird) to view the images as attachments when displaying the
        # message as plaintext, without it interrupting those users who view
        # it as HTML.
        image.add_header(
            'Content-Disposition', 'attachment; filename=%s' % filename
        )

        # Attach the image.
        email.attach(image)

    # Finally, send the message.
    email.send(fail_silently)
