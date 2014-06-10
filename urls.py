# -*- coding: utf8 -*-
from django.conf.urls import patterns, url
from userforms import views

urlpatterns = patterns('',
    # список новостей
    url(r'^$', views.index, name='userforms_index'),
    url(r'^success/$', views.success, name='userforms_success'),

)