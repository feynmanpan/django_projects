# -*- coding: utf-8 -*- 

from django.db import models
from django.utils import timezone

# Create your models here. 
# default: 表單欄位幫你填入的值
# blank  : 是否允許表單欄位不填，空欄位以 '' 傳DB 
# null   : False時，''照存 
#          True時，為 - ，不存''
# 所以文字欄位可blank時，用null=False保持以''存取，所有操作只有非空及空字串兩種情形
# max_length: 字數(unicode數)，不是byte數 

class Store(models.Model):
    code      = models.CharField(default='00',max_length=2)
    name      = models.CharField(max_length=200)
    url       = models.URLField( default=None, blank=True, null=False)    
    url_logo  = models.URLField( default=None, blank=True, null=False)
    url_href  = models.CharField(default=None, blank=True, null=False,max_length=100)
    create_dt = models.DateTimeField(default=timezone.now,verbose_name='建立日期')	

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('code',)		
		
	

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
