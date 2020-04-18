from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.


def homepage(request):
    posts = Post.objects.all()
    post_list = []
    for c, post in enumerate(posts):
        post_list.append(f"No.{str(c)+': '+str(post)+'<br>'}")
        post_list.append("<h1>"+post.body+"</h1>")

    #
    return HttpResponse(post_list)
    #now = datetime.now()
    # return render(request, 'index.html', locals())
