import os
import sys
import requests
from pyquery import PyQuery as pq
from google_drive_downloader import GoogleDriveDownloader as gdd
from datetime import datetime, timedelta


def get_xlsx_name(report_date):
    wd = ['一', '二', '三', '四', '五', '六', '日']
    idxwd = (report_date + timedelta(days=1)).weekday()
    #
    d1 = report_date - timedelta(days=6)
    d1_date = d1.date()
    y1 = d1_date.year-1911
    m1 = d1_date.month
    d1 = d1_date.day
    s1 = f'{y1}.{m1:02}.{d1:02}'
    #
    d2 = report_date
    d2_date = d2.date()
    y2 = d2_date.year-1911
    m2 = d2_date.month
    d2 = d2_date.day
    s2 = f'{y2}.{m2:02}.{d2:02}'
    #
    fn = f'{s1}-{s2}價格週{wd[idxwd]}.xlsx'
    #
    return fn


def download_xlsx(year=2020, month=4, day=20, save_xlsx_path=None):
    # report_date = datetime(year, month, day)
    url = f'https://aprp.atri.org.tw/dailytrans/daily-report/render/?day={day}&month={month}&year={year}'
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    #
    r = requests.get(url,
                     headers=header,
                     timeout=60)
    r.encoding = 'utf8'

    rtext = r.text
    if '<html>' not in rtext:
        rtext = '<html>'+rtext+'</html>'
    #
    doc = pq(rtext)
    iframe = doc.find("iframe")
    src = iframe.attr("src")
    fid = src.split('/')[-2]
    # src_download = f'https://drive.google.com/u/0/uc?id={fid}&export=download'

    # 預設下載到桌面
    gdd.download_file_from_google_drive(file_id=fid, dest_path=save_xlsx_path)


if __name__ == '__main__':
    report_date_str = (len(sys.argv) > 1 and sys.argv[1]) or None
    save_xlsx_path = (len(sys.argv) > 2 and sys.argv[2]) or None
    #
    if report_date_str: #20200420
        y = int(report_date_str[:4])
        m = int(report_date_str[4:6])
        d = int(report_date_str[6:8])
        report_date = datetime(y, m, d)
    else:
        report_date = (datetime.today() + timedelta(days=-1))
        y = report_date.year
        m = report_date.month
        d = report_date.day
    #
    if not save_xlsx_path:
        save_xlsx_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', get_xlsx_name(report_date))
    else:
        # 只打folder就好
        save_xlsx_path = os.path.join(save_xlsx_path, get_xlsx_name(report_date))
    #
    print('報表日期=', y, m, d)
    print('Excel儲存路徑=', save_xlsx_path)
    download_xlsx(y, m, d, save_xlsx_path)
    print('下載完成')
    print('________________________________________________________')
