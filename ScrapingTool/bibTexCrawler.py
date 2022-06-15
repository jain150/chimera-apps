from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import pandas as pd
from bs4 import BeautifulSoup
import os
import re
import requests
import urllib.request
import time
from PyPDF2 import PdfFileReader
import subprocess
import shutil
from fake_useragent import UserAgent





PROXY = "46.21.153.16:3128"
# option = webdriver.ChromeOptions()
# option.add_argument('--proxy-server=%s' % PROXY)

prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.autodetect = False
capabilities = webdriver.DesiredCapabilities.CHROME
prox.http_proxy = PROXY
prox.ssl_proxy = PROXY
prox.add_to_capabilities(capabilities)


#Adding Spoofing stuff (hiding automation software use)

option = webdriver.ChromeOptions()
#window-size
option.add_argument("window-size=1280,680")
#navigator undefined
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
option.add_argument('--disable-blink-features=AutomationControlled')

#User Agent Spoof
# agent = UserAgent()
# randomAgent = agent.random

# print(randomAgent)  #TODO: Remove, testing

option.add_argument(f'user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36')

driver = webdriver.Chrome('/Users/Arnav/Desktop/Work/chromedriver', options = option)


##### MODIFY 'start' with increments of 10 to go to next page, Pg 1 == 0 #####
WEBPAGE = 'https://scholar.google.com/scholar?start=100&q=wearables&hl=en&as_sdt=0,22'

driver.get(WEBPAGE)

blocks = driver.find_elements_by_class_name("gs_or_cit")

for block in blocks:

    #Clicking on cite button (")
    block.click()
    time.sleep(10)

    #Saving "BibTeX" url
    bibtexUrl = driver.find_element_by_link_text("BibTeX").get_attribute('href')

    #Opening new tab
    driver.execute_script("window.open('');")
    #Switching to new window
    driver.switch_to.window(driver.window_handles[1])
    #Opening previously saved bibtexUrl
    driver.get(bibtexUrl)

    #TODO: Save/Parse src code
    f = open('testerBibtex.txt', 'w')
    f.write(driver.page_source)
    f.close
    print("DONE\n")

    time.sleep(10)

    #Closing tab
    driver.close()
    #Switching back to initial tab
    driver.switch_to.window(driver.window_handles[0])

    #Clicking on the cross (x) to close modal
    time.sleep(3)               #TODO: REMOVE
    driver.find_element_by_class_name("gs_ico").click()
    time.sleep(2)
