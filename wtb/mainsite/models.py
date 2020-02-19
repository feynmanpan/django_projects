# -*- coding: utf-8 -*- 

from django.db import models
from django.utils import timezone

# Create your models here. 


class Store(models.Model):
    name      = models.CharField(max_length=200)
    url       = models.URLField(default='')    
    url_logo  = models.URLField(default='')
    create_dt = models.DateTimeField(default=timezone.now,verbose_name='建立日期')	

    def __str__(self):
        return self.name

class Post(models.Model):
    AA = models.CharField(max_length=200,default='')
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now,verbose_name='張貼日期')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
