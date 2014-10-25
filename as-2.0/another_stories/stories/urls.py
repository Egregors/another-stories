# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include

from stories import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<story_id>\d+)/$', views.story, name='story'),
    url(r'^(?P<story_id>\d+)/like/$', views.like, name='like'),
)