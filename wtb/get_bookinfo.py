#%load get_bookinfo.py
#_____________________
import os
import django
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wtb.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from mainsite.models import Store
#import mainsite.models


#__________________________
stores = Store.objects.all().order_by('code')
for s in stores:
    print(s.code)
