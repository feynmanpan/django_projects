from django.shortcuts import render, redirect
from datetime import datetime
from .models import Post

# Create your views here.
def homepage(request):
    posts = Post.objects.all()
    #now = datetime.now()
    return render(request, 'index.html', locals())
	
def showpost(request, slug):
	try:
		now = datetime.now()
		post = Post.objects.get(slug = slug)
		if post:
			return render(request, 'post.html', locals())
	except:
		return redirect('/index')	


