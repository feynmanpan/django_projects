import os
#
from fastapi.templating import Jinja2Templates
#
##########################################################


dt_format = "%Y-%m-%d_%H:%M:%S"
pub_dt_format = "%Y-%m-%d"
#
cwd = os.path.dirname(os.path.realpath(__file__))
templates = 'templates'
jinja_templates = Jinja2Templates(directory=os.path.join(cwd, templates))
#
timeout = 7
update_errcnt_max = 5
