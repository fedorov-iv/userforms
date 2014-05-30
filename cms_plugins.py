# -*- coding: utf8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from userforms.models import UserForms, UserForm
from userforms.forms import FunkyForm
from django.http import HttpResponseRedirect
from userforms.middleware.force_redirect import ForceResponse
from django.core.urlresolvers import reverse


class UserFormsPlugin(CMSPluginBase):
    """ Plugin: Displays admin edited forms"""
    model = UserForms
    name = 'User Forms'
    render_template = "plugins/user_forms.html"
    cache = False

    def render(self, context, instance, placeholder):
        user_form = UserForm.objects.get(pk=instance.user_form.id)
        form = FunkyForm(user_form=user_form)
        request = context['request']

        # If POST and we see that it is our form then validate and save data to database
        if request.method == 'POST' and request.POST.get('user_form_id') and int(request.POST.get('user_form_id')) == user_form.id:
            form.data = request.POST.copy()
            form.files = request.FILES.copy()
            form.is_bound = True

            if form.is_valid():
                form.save(user_form=user_form)  # Saving to database

                raise ForceResponse(HttpResponseRedirect('/'))

            else:
                context['form_meta'] = user_form
                context['form'] = form
                return context
        else:
            # showing form
            context['form_meta'] = user_form
            context['form'] = form
            return context

plugin_pool.register_plugin(UserFormsPlugin)