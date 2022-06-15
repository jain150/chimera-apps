from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import os
import re
import requests
import urllib.request
import time


files = ["scholar_src-code.txt", "scholar_pdfs.txt", "parsed_data-lid.txt"]
for f in files:
    if os.path.exists(f):
        os.remove(f)
    else:
        print("File '%s' does not exist." %f)

try:

    #User-Agent Spoofing
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'

    driver = webdriver.Chrome('/Users/Arnav/Desktop/Work/chromedriver')
    driver.get('https://scholar.google.com/scholar?start=50&q=wearables&hl=en&as_sdt=0,22')

    srcCode = driver.page_source

    #<scroll page down snippet>
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page
        time.sleep(2)
        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()

    #BeautifulSoup instance
    soup = BeautifulSoup(srcCode, 'lxml')

    f = open("parsed_data-lid.txt", 'w')
    i = 1;

    for item in soup.select('[data-lid]'):
        f.write('_______________________________________________________________' + "\n")
        f.write(str(i) + '.')
        f.write(item.select('h3')[0].get_text() + "\n")
        f.write(item.select('a')[0]['href'] + "\n")
        f.write(item.select('.gs_rs')[0].get_text() + "\n")
        f.write('_______________________________________________________________' + "\n")
        i = i + 1;

    f.close


    #testing
    for item in soup.select('[data-lid]'):
        print('_________________________________________________________________')
        print(item.select('h3')[0].get_text())
        print(item.select('a')[0]['href'])
        print(item.select('.gs_rs')[0].get_text())
        print('_________________________________________________________________')


    f.close


except Exception as e:
    print(str(e))
