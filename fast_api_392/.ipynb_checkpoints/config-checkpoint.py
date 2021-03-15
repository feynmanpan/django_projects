from enum import Enum
#


class MODES(Enum):
    maintenance = 1
    debug = 2
    prod = 3


now_mode = MODES(3)  # MODES.maintenance, MODES['maintenance']


maintenance_allow_patterns = [
    '^/test/.+',
    '^/static/.+',
]


allowed_hosts = [
    "wtb.wtbwtb.tk",
]
# True在main啟動時就執行
startBGT_atonce = False