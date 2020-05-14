# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import requests
import pyquery
from get_proxy import get_proxy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select #處理下拉
from selenium.webdriver.chrome.service import Service #
import os


# option____________________________________________
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')  # 让Chrome在root权限下跑
chrome_options.add_argument("--window-size=500,1024") #太寬會有chrome的render報錯
# chrome_options.add_argument("window-size=1024x1024")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--headless')  # 不用打开图形界面
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument("enable-features=NetworkServiceInProcess")
# chrome_options.add_argument("disable-features=NetworkService")
#
# ippo=get_proxy(which='free',now=True)
# chrome_options.add_argument(f'--proxy-server={ippo}')
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
chrome_options.add_argument(f"user-agent={ua}")


try:
    # driver____________________________________________
    # 記得查chrome版本，用同版本的driver:google-chrome -version
    driver_path='/home/pan/chromedriver81'
#     c_service = Service(driver_path)
#     c_service.command_line_args()
#     c_service.start()    
#     driver = webdriver.Remote(c_service.service_url,options=chrome_options)    
    driver = webdriver.Chrome(driver_path, options=chrome_options)
    driver.implicitly_wait(5)
    url_freeproxylist = "https://free-proxy-list.net/"
    #
    driver.get(url_freeproxylist)
    print('目前網址:', driver.current_url)
    # print('頁面內容',driver.page_source)

    # 選擇 elite =================================================================================
    select = "#proxylisttable > tfoot > tr > th:nth-child(5) > select"
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, select)))
    elite_proxy = Select(driver.find_element_by_css_selector(select))
    elite_proxy.select_by_value("elite proxy")
    elite_proxy_val = elite_proxy.first_selected_option.text

    print('選擇elite proxy:', elite_proxy_val)

    # 頁數 =================================================================================
    # li_pagenum_last = "#proxylisttable_paginate > ul > li:last-child"
    li_pagenum_last = '//*[@id="proxylisttable_next"]/preceding-sibling::li[1]'
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, li_pagenum_last)))
    li_last = driver.find_element_by_xpath(li_pagenum_last)
    pagenum_last = int(li_last.text)

    print('總頁碼:', pagenum_last)
    pagenum_last=1

    # ippo =================================================================================
    ippos = []
    table_tr = "#proxylisttable_wrapper tbody tr"
    for pn in range(1, pagenum_last+1):
        print('目前頁碼:', pn)
        # page_btn=f"a[data-dt-idx='{pn+1}']"
        page_btn = f'//*[@id="proxylisttable_paginate"]/ul//a[@data-dt-idx and text()="{pn}"]'
        button_page = driver.find_element_by_xpath(page_btn)
        button_page.click()
        # 等表出來
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, table_tr)))
        trs = driver.find_elements_by_css_selector(table_tr)
        for tr in trs:
            ip = tr.find_element_by_xpath(".//td[1]").text
            po = tr.find_element_by_xpath(".//td[2]").text
            ippos.append(ip+":"+po)
    #
    print('ippo個數:', len(ippos))

    # TXT =================================================================================
    fn = 'ips_free_test.txt'
    with open(fn, 'r+') as f:
        new = "\n".join(ippos)
        old = "".join(f.readlines()[:-len(ippos)])
        now = new+'\n'+old
        f.seek(0)  # 從頭寫入
        f.write(now)
        f.truncate()  # 寫入最後一行之後都不要
    print('ips_free更新')

except Exception as err:
    print('連線問題:', err)
finally:
    # quit____________________________________________
    try:
        
#         print(driver.window_handles)
#         print(driver.current_window_handle)
#         now_handle=driver.current_window_handle
#         driver.switch_to.window(now_handle)
  
#         driver.close()
        driver.quit()        
#         c_service.stop()        
        os.system('pkill chrome')
        print("clsoe")
    except Exception as err:
        print("close有問題", err)
        driver.quit()

