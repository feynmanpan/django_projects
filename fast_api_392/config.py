from enum import Enum
from os import path
#
templates = 'templates'
static_html = 'static_html'


class MODES(Enum):
    maintenance = 1
    debug = 2
    prod = 3


now_mode = MODES(1)  # MODES.maintenance, MODES['maintenance']
maintenance_allow_patterns = [
    '^/test/.+',
    '^/static/.+',
]
maintenance_html = 'maintenance.html'


check_isTH_name = 'check_isTH'
trusted_host = True
allowed_hosts = [
    "wtb.wtbwtb.tk",
    "34.80.136.230",
]


# True在main啟動時就執行
startBGT_atonce = False
