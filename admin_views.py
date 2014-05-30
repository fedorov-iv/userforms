# -*- coding: utf8 -*-
from userforms.models import UserFormField
from django.http import HttpResponse
import json


# ajax requested view, which saves options for a select field
def save_options(request, userform_id=0, userformfield_id=0):
    values = request.POST.get('values')
    if values:
        user_form_field = UserFormField.objects.get(pk=userformfield_id)
        user_form_field.choices = values
        user_form_field.save()
        return HttpResponse(json.dumps(['ok']), content_type="application/json")
    else:
        return HttpResponse(json.dumps(['no options received']), content_type="application/json")


# ajax requested view, which returns saved options for a select field
def get_options(request, userform_id=0, userformfield_id=0):
    user_form_field = UserFormField.objects.get(pk=userformfield_id)
    if user_form_field.choices:
        return HttpResponse(user_form_field.choices, content_type="application/json")
    else:
        return HttpResponse('0', content_type="application/json")