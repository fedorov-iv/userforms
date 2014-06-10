userforms
=========

Django CMS AppHook for generating web-forms from django-cms admin.

Supported form fields:
 * Text
 * E-mail
 * Textarea
 * Checkbox
 * List (combobox)
 * File
 * Captcha

First there was an idea to make a CMSPlugin, but I faced redirection problems from plugin render method
(Yes, I know there is a workaround, using exception and additional middleware).

### Insallation

    INSTALLED_APPS = (
           ...
            'userforms',
            ...
    )

Captcha Field needs django-simple-captcha with dependencies (PIL, Pillow) to be installed and activated in settings.py

    INSTALLED_APPS = (
           ...
            'captcha',
            ...
    )
