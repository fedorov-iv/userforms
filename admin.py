# -*- coding: utf8 -*-
from django.contrib import admin
from userforms.models import UserForm, UserFormField, UserFormAnswer, UserFormAnswerValue
from filters import UserFormListFilter
from django.conf.urls import patterns, url
from userforms import admin_views


class UserFormFieldInline(admin.StackedInline):
    model = UserFormField
    extra = 0
    exclude = ('choices', )

    class Media:
        js = (
            '/static/userforms/js/scripts.js',
        )


class UserFormsAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_to_answers', 'is_active')
    search_fields = ['title']
    inlines = [UserFormFieldInline]

    # Add urls for ajax-requests that get and save options for select fields. See admin_views.py.
    def get_urls(self):
        admin_urls = super(UserFormsAdmin, self).get_urls()
        new_admin_urls = patterns('',
            url(r'^(?P<userform_id>\d+)/saveoptions/(?P<userformfield_id>\d+)/$', admin_views.save_options, name='save_options'),
            url(r'^(?P<userform_id>\d+)/getoptions/(?P<userformfield_id>\d+)/$', admin_views.get_options, name='get_options'),
        )
        return new_admin_urls + admin_urls


class UserFormAnswerValueInline(admin.StackedInline):
    model = UserFormAnswerValue
    extra = 0
    exclude = ('user_form', 'user_form_field', 'answer')
    readonly_fields = ('formatted_answer',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserFormAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'related_answers', 'is_active')
    list_filter = ('is_active', 'create_date', UserFormListFilter)
    list_per_page = 5
    readonly_fields = ('user_form',)
    fields = ('user_form', 'create_date', 'is_active')
    inlines = [UserFormAnswerValueInline]

    def has_add_permission(self, request):
        return False

admin.site.register(UserForm, UserFormsAdmin)
admin.site.register(UserFormAnswer, UserFormAnswerAdmin)