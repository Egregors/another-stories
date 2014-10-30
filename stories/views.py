import json
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from stories.models import Story


def index(request):
    stories_list = Story.objects.all()
    paginator = Paginator(stories_list, 2)

    page = request.GET.get('page')
    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        stories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        stories = paginator.page(paginator.num_pages)

    return render(request, 'stories/index.html', {'stories': stories})


def story(request, story_id):
    story = Story.objects.get(pk=story_id)
    return render(request, 'stories/story.html', {'story': story})


def like(request, story_id):
    story = Story.objects.get(pk=story_id)
    story.add_like()
    story.save()
    return redirect('index')
