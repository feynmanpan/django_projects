# -*- coding: utf-8 -*- 

from django.db import models
from django.utils import timezone

# Create your models here. 
# default: admin表單欄位幫你填入的值，還有ORM時的預設值
# blank  : False時，admin會擋none及''                     
#          ORM無關                
# null   : False時，admin: None    > ''  !!!!
#                          ''      > ''
#                  ORM 擋  None 
#          True時，admin:  None    > -
#                          ''      > -   !!!!
#                  ORM:    None    > - 
#                          ''      > ''
# 所以null=False保持以''存取，所有操作只有非空及空字串兩種情形
# max_length: 字數(unicode數)，不是byte數    

class Bookinfo(models.Model):
    #博客來的店內碼做PK
    err       = models.CharField(default='', blank=True, null=False, max_length=100)
    bookid    = models.CharField(primary_key=True,default='',max_length=10) 
    isbn      = models.CharField(unique=False,default='',max_length=13)
    title     = models.CharField(max_length=200)
    author    = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    url_cover = models.URLField(default='', blank=True, null=False)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ('bookid',)	


class Store(models.Model):
    code      = models.CharField(default='00',max_length=2)
    name      = models.CharField(max_length=200)
    url       = models.URLField( default='', blank=True, null=False)    
    url_logo  = models.URLField( default='', blank=True, null=False)
    url_href  = models.CharField(default='', blank=True, null=False,max_length=100)
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
