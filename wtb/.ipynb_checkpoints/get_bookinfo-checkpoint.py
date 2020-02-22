# -*- coding: utf-8 -*- 

import os
import django
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wtb.settings')
django.setup()
from mainsite.models import Store
#import mainsite.models


#__________________________
stores = Store.objects.all().order_by('code')
print(stores)