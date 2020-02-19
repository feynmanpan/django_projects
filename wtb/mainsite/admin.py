from django.contrib import admin
from .models import Store,Post
# Register your models here

class StoreAdmin(admin.ModelAdmin):
    list_display=('name','url','url_logo','create_dt')

class PostAdmin(admin.ModelAdmin):
    list_display=('AA','title','slug','pub_date')


admin.site.register(Post,PostAdmin)
admin.site.register(Store,StoreAdmin)
