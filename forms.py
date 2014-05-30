from userforms.models import UserFormField, UserFormAnswer, UserFormAnswerValue
from django import forms
from captcha.fields import CaptchaField
from django.conf import settings
import os
import json


class FunkyForm(forms.Form):

    def __init__(self, user_form, *args,  **kwargs):
        super(FunkyForm, self).__init__(*args, **kwargs)

        self.fields['user_form_id'] = forms.CharField(widget=forms.HiddenInput(attrs={'value': user_form.id}))

        for q in UserFormField.objects.filter(user_form=user_form).order_by('order'):
            if q.field_type == 'text':
                self.fields['form_{0}_field_{1}'.format(user_form.id, q.id)] = forms.CharField(label=q.title, required=q.is_required)
            elif q.field_type == 'email':
                self.fields['form_{0}_field_{1}'.format(user_form.id, q.id)] = forms.EmailField(label=q.title, required=q.is_required)
            elif q.field_type == 'textarea':
                self.fields['form_{0}_field_{1}'.format(user_form.id, q.id)] = forms.CharField(label=q.title, widget=forms.Textarea, required=q.is_required)
            elif q.field_type == 'checkbox':
                self.fields['form_{0}_field_{1}'.format(user_form.id, q.id)] = forms.BooleanField(label=q.title, required=q.is_required)
            elif q.field_type == 'file':
                self.fields['form_{0}_field_{1}'.format(user_form.id, q.id)] = forms.FileField(label=q.title, required=q.is_required)
            elif q.field_type == 'captcha':
                self.fields['form_{0}_field_{1}'.format(user_form.id, q.id)] = CaptchaField(label=q.title)
            elif q.field_type == 'select':
                ch = json.loads(q.choices).items()
                self.fields['form_{0}_field_{1}'.format(user_form.id, q.id)] = forms.ChoiceField(label=q.title, choices=ch,  required=q.is_required)

    def save(self, user_form):
        user_form_answer = UserFormAnswer()
        user_form_answer.user_form = user_form
        user_form_answer.save()

        #  File uploads
        if self.files:
            self.handle_uploaded_files(user_form_answer)

        for key, value in self.cleaned_data.items():
            if key.startswith('form'):
                key_list = key.split('_')
                user_form_answer_value = UserFormAnswerValue()
                user_form_answer_value.user_form = user_form
                user_form_answer_value.user_form_answer = user_form_answer
                user_form_answer_value.user_form_field = UserFormField.objects.get(pk=key_list[3])
                user_form_answer_value.answer = value if value else ''
                user_form_answer_value.save()

    def handle_uploaded_files(self, user_form_answer):
        files_dir = os.path.join(settings.MEDIA_ROOT, 'userforms', 'userformanswer_{0}'.format(user_form_answer.id))
        if not os.path.exists(files_dir):
            os.makedirs(files_dir)
        for key, f in self.files.items():
            with open(files_dir + '/' + f.name, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)