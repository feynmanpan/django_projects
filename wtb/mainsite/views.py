from django.shortcuts import render, redirect
from datetime import datetime
from .models import Post

# Create your views here.
def homepage(request,now):
    posts = Post.objects.all()
    now = now#datetime.now()
    return render(request, 'index.html', locals())


