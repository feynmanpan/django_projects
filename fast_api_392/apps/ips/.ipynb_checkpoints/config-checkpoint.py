import os

#
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
}
url_free = 'https://free-proxy-list.net/'

cacert = True

cwd = os.path.dirname(os.path.realpath(__file__))
ips_csv = os.path.join(cwd, 'ips.csv')
ips_html = os.path.join(cwd, 'ips.html')
