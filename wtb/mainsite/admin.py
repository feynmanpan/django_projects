from django.contrib import admin
from .models import Bookinfo,Bookprice,Store,Post
# Register your models here

class BookinfoAdmin(admin.ModelAdmin):
    list_display=('bookid','err','isbn','title','author','publisher','pub_dt','price_list','price_sale','price_sale_ebook','bookid_ebook','create_dt')

class BookpriceAdmin(admin.ModelAdmin):
    list_display=('bookid','err','isbn','store','price_sale','price_sale_ebook','url_book','url_ebook','create_dt')


class StoreAdmin(admin.ModelAdmin):
    list_display=('name','code','url','url_logo','url_href','create_dt')

class PostAdmin(admin.ModelAdmin):
    list_display=('AA','title','slug','pub_date')

#
admin.site.register(Bookinfo,BookinfoAdmin)
admin.site.register(Bookprice,BookpriceAdmin)
admin.site.register(Store,StoreAdmin)
admin.site.register(Post,PostAdmin)