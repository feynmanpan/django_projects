#%load get_bookinfo.py
#_____________________
import os
import django
from django.utils import timezone
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wtb.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from mainsite.models import Store,Post
#import mainsite.models


#__________________________
stores = Store.objects.all().order_by('code')
#print(type(stores))
for s in stores:
    print(s.name)
    
#p = Post.objects.create(AA='swsw',title='dede',slug='1234',body='dede',pub_date=timezone.now)
#p.save()
