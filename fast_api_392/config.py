from enum import Enum
#
class Modes(Enum):
    maintenance = 1
    debug = 2
    prod = 3


now_mode = Modes(3)  # 　Modes.maintenance, Mode['maintenance']
#

maintenance_allow_patterns = [
    '^/test/.+',
    '^/static/.+',
]