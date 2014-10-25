#-*- coding: utf-8 -*-

from django.db import models

class Story(models.Model):
    title = models.CharField(u'Название истории', max_length=600)
    text = models.TextField(u'Сама история')
    like = models.IntegerField(u'Лайки', default=0)
    timestamp = models.DateTimeField(u'Время добавления')

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = u'удивительные истории'
        verbose_name_plural = u'истории'

    def add_like(self):
        self.like += 1

    def __unicode__(self):
        return self.title