from django.contrib import admin
from .models import Bookinfo,Store,Post
# Register your models here

class BookinfoAdmin(admin.ModelAdmin):
    list_display=('bookid','err','isbn','title','author','publisher','pub_dt','create_dt')

class StoreAdmin(admin.ModelAdmin):
    list_display=('name','code','url','url_logo','url_href','create_dt')

class PostAdmin(admin.ModelAdmin):
    list_display=('AA','title','slug','pub_date')

#
admin.site.register(Bookinfo,BookinfoAdmin)
admin.site.register(Store,StoreAdmin)
admin.site.register(Post,PostAdmin)