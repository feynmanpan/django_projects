import os
import itertools
#
from fastapi.templating import Jinja2Templates
########################################################
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
}
# 
url_free = [
    "https://www.sslproxies.org/",
    'https://free-proxy-list.net/',
    'https://www.us-proxy.org/',    
]
url_free_cycle = itertools.cycle(url_free)
level_https = [
    ('anonymous', 'yes'),
    ('elite proxy', 'yes'),
#     ('anonymous', 'no'),
#     ('elite proxy', 'no'),    
]
get_freeproxy_delta = 4*60
timeout = 15
proxy_checkurls = [
    "http://210.240.175.62/NTIIS/IP_test.asp",
    "https://whatismyipaddress.com/zh-cn/index",
    "https://httpbin.org/ip",
    "https://www.whatismyip.com.tw/tw/",
    "https://www.whatismyip.com/",
    "https://www.rus.net.tw/myip.php",
    "https://www.expressvpn.com/what-is-my-ip",
]
sampleN = len(proxy_checkurls)
check_atleast = 1
#
cacert = [False, True][1]
#
cwd = os.path.dirname(os.path.realpath(__file__))
templates = 'templates'
jinja_templates = Jinja2Templates(directory=os.path.join(cwd, templates))
#
ips_csv = 'ips.csv'
ips_html = 'ips.html'
ips_csv_tb_html = 'ips_csv_tb.html'
#
ips_csv_path = os.path.join(cwd, ips_csv)
ips_html_path = os.path.join(cwd, templates, ips_html)
#
ips_cycle = False
dtype = {'port': str}
dt_format = "%Y-%m-%d_%H:%M:%S"
ipcols = ['ip', 'port', 'now']
maxN = 500

