"""wtb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf    
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')) 
"""
from django.contrib import admin
from django.urls import path,include
from mainsite.views import wtb_index,wtb_book,wtb_search,wtb_autocom,wtb_tpml,wtb_hybook,get_client_ip,homepage, homepage_1,homepage_2,showpost,showpost_1


test_patterns=[
    path('<str:AAA>/', homepage_1,name='test-url'),
]

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', wtb_index),
    path('book/<str:bookid>/', wtb_book),
    path('search/', wtb_search),
    path('autocom/', wtb_autocom),
    path('tpml/', wtb_tpml),
    path('hybook/<int:page>/', wtb_hybook),
    path('get_client_ip/', get_client_ip),
    #
    path('index/<str:test>/', homepage),
    #path('index_1/', homepage_1,{'AAA':2345}),
    #path('index_1/', include(test_patterns)),
    path('index_2/<str:AAA>/<str:BBB>', homepage_2,name='test-url'),
    path('post/<slug:slug>/', showpost),
    path('post_1/<slug:slug>/', showpost_1),
]
