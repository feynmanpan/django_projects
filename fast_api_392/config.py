from enum import Enum
import os
#
from fastapi.templating import Jinja2Templates
#
top_dir = os.getcwd()
static = 'static'
templates = 'templates'
static_html = 'static_html'  # 在templates中的子目錄
#
jinja_templates = Jinja2Templates(directory=templates)


class MODES(Enum):
    maintenance = 1
    debug = 2
    prod = 3


now_mode = MODES(3)  # MODES.maintenance, MODES['maintenance']
maintenance_allow_patterns = [
    '^/test/.+',
    '^/static/.+',
]
maintenance_html = 'maintenance.html'


check_isTH_name = 'check_isTH'
trusted_host = [True, False][0]
allowed_hosts = [
    "wtb.wtbwtb.tk",
    "34.80.136.230",
]


# True在main啟動時就執行
startBGT_atonce = [True, False][0]
get_freeproxy_delta = 8*60
