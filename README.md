# About

Markdown-mail support for [Django](https://www.djangoproject.com/) via [`mdmail`](https://github.com/yejianye/mdmail).

Django is a popular web framework which contains its own wrapper functions for sending email, written in Python.

`mdmail` is a Python library for sending email in both plaintext and HTML forms, using glorious markdown.

This simple library wraps those two elements together, allowing users of Django to easily use Django's built-in facilities to send email in markdown instead of a combination of plaintext and HTML.

The most important design goal of this library is to allow a Django user to replace...

    from django.core.mail import send_mail

...with...

    from django_mdmail import send_mail

...to send markdown emails with all the features of the Django email functionality intact.

# Installation

    pip install django_mdmail

# Notes on parameters

## Parameters from `mdmail`

### `css`

The parameter `css` can be used with both the `send_mail` and `convert_md_templates` functions, which then gets moved forward to `mdmail`'s underlying function, `EmailContent`. The `css` parameter should contain **CSS as text**, not as a filename.

## Parameters from `django.core.mail.send_mail`

### `html_message`

The parameter `html_message` can be used with the `send_mail` function to override the HTML generated from markdown, although that completely defies the whole point of using `django_mdmail` in the first place. It is provided for API compatibility.

# Template-driven emails

In Django and some libraries written for it, emails are formed from Django templates, such as for confirmations of various sorts and resetting forgotten passwords. Such mechanisms typically assume one template for plaintext emails and another one for HTML emails, forcing a Django user to maintain two separate versions of the same content, one in plaintext and one in HTML.

Using this library, a single markdown file can be written with an `.md` filename ending which is then generated into both a `.txt` version and `.html` version when a Django server is started. This is done through AppConfig as per the following example, where the app's name is `core` and the following contents are in `core/apps.py`:

    from django.apps import AppConfig
    from django_mdmail import convert_md_templates

    class CoreConfig(AppConfig):
        name = 'core'

        # A function that is run by Django at server startup (not per page hit).
        def ready(self):
            # Converts markdown templates (`.md`) into plaintext (`.txt`) and HTML (`.html`) templates.
            convert_md_templates()

*Note: If you copy-paste this code and your app's name is "whatever", you need to replace "core" with "whatever" and "CoreConfig" with "WhateverConfig". See the [documentation on `AppConfig.ready()`](https://docs.djangoproject.com/en/3.2/ref/applications/#methods) for details.*

Assuming that this code runs without failure, then all you need to do in order to get markdown-generated `.txt` and `.html` templates, is to write a template in markdown using the file ending `.md` in a proper template directory. It will be chopped down into corresponding `.txt` and `.html` files which will then be used by whatever internal or built-in email functionality you are using.

# Images

1. Images by URL are supported, with the caveat that if a user is using a responsible email client that respects people's privacy, the images will not be automatically shown, but only if the user specifically requests them. This may be problematic for a message that relies too heavily on images for either communication or aesthetics.

2. Inline images are supported but they must be available on the server that sends the email (the Django server) and the image link in the markdown message must be relative to the Django project's root. This is partly a limitation of `mdmail`, but if you host your images on the same server as the Django instance that sends the emails, **you can indeed** use inline images that even the most annoyingly responsible email clients will display, assuming they render HTML in the first place.

## Known limitations

Inline images are not supported in emails rendered from templates.
