from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from stories.models import Story


class StoriesAdmin(SummernoteModelAdmin):
    list_filter = ['timestamp']

admin.site.register(Story, StoriesAdmin)