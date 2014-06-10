# -*- coding: utf8 -*-
from django.db import models
import datetime
from django.conf import settings
from cms.models import Page


class UserForm(models.Model):
    cms_pages = models.ManyToManyField(Page, limit_choices_to={'publisher_is_draft': True}, blank=True, null=True)
    title = models.CharField('Title', max_length=255)
    text_before = models.TextField('Text above form', blank=True)
    text_after = models.TextField('Text below form', blank=True)
    text_after_send = models.TextField('Text after sending form', blank=True)
    create_date = models.DateTimeField('Created', default=datetime.datetime.now())

    class Meta:
        verbose_name = 'Form'
        verbose_name_plural = 'Forms'
        ordering = ['title']

    def link_to_answers(self):
        return '<a href="/admin/userforms/userformanswer/?userform={0}">{1} => </a>'.format(self.pk, self.answers_count())

    link_to_answers.short_description = 'Answers'
    link_to_answers.allow_tags = True

    def answers_count(self):
        return UserFormAnswer.objects.filter(user_form=self.pk).count()

    def __unicode__(self):
        return self.title


class UserFormField(models.Model):

    USER_FORM_FIELD_TYPES = (
        ('text', 'Text'),
        ('email', 'E-mail'),
        ('textarea', 'Text area'),
        ('checkbox', 'Checkbox'),
        ('captcha', 'Captcha'),
        ('file', 'File'),
        ('select', 'List'),
    )
    user_form = models.ForeignKey(UserForm)
    title = models.CharField('Title', max_length=255)
    field_type = models.CharField('Field type', choices=USER_FORM_FIELD_TYPES, max_length=255, )
    is_required = models.BooleanField('Required', default=False)
    order = models.PositiveSmallIntegerField('Ordering', default=0)
    show_in_list = models.BooleanField('Show in answers list', default=False)
    choices = models.CharField(blank=True, max_length=1000)  # choices' values for select fields

    class Meta:
        verbose_name = 'Form field'
        verbose_name_plural = 'Form fields'
        ordering = ['order']

    def __unicode__(self):
        return self.title


class UserFormAnswer(models.Model):
    user_form = models.ForeignKey(UserForm, verbose_name='Form')
    create_date = models.DateTimeField('Created', default=datetime.datetime.now())

    class Meta:
        verbose_name = 'Form answer'
        verbose_name_plural = 'Form answers'
        ordering = ['-create_date', '-id']

    def related_answers(self):
        answer_values = UserFormAnswerValue.objects.filter(user_form_answer__id=self.id, user_form_field__show_in_list=True)
        formatted_str = u'<table style="border-width:0; width:0">'
        for a in answer_values:
            formatted_str += u'<tr><td style="border-width:0; padding:0">{0}: </td><td style="border-width:0; padding:0">{1}</td></tr>'.format(a.user_form_field.title, a.formatted_answer())
        formatted_str += u'</table>'
        return formatted_str

    related_answers.short_description = 'Form data'
    related_answers.allow_tags = True

    def __unicode__(self):
        return self.user_form.title


class UserFormAnswerValue(models.Model):
    user_form = models.ForeignKey(UserForm, verbose_name='Form')
    user_form_field = models.ForeignKey(UserFormField, verbose_name='Form field')
    user_form_answer = models.ForeignKey(UserFormAnswer, verbose_name='Form answer')
    answer = models.TextField('Value', blank=True, default='', null=True)

    def formatted_answer(self):
        if self.user_form_field.field_type == 'file':
            return u'<a href="{0}" target="_blank">{1}</a>'.format(settings.MEDIA_URL + u'userforms'+ u'/userformanswer_{0}'.format(self.user_form_answer.id) + u'/' + self.answer, self.answer)
        elif self.user_form_field.field_type == 'checkbox':
            return 'Yes' if self.answer == 'True' else 'No'
        else:
            return self.answer

    formatted_answer.short_description = 'Value'
    formatted_answer.allow_tags = True

    class Meta:
        verbose_name = 'Form data'
        verbose_name_plural = 'Form data'
        ordering = ['user_form_field__order']

    def __unicode__(self):
        return self.user_form_field.title
