from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', include('stories.urls')),

    url(r'^stories/', include('stories.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^summernote/', include('django_summernote.urls')),

)
