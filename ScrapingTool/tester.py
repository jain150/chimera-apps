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


# #User-Agent Spoofing
# headers = {}
# headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'



# opener = urllib.request.URLopener()
# opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0')]
# #urllib.request.install_opener(opener)
#
# opener.retrieve('https://www.futuremedicine.com/doi/pdfplus/10.2217/pme-2018-0044', "testPDF.pdf")


# urllib.request.urlretrieve('https://onlinelibrary.wiley.com/doi/pdf/10.1002/adma.201706910', "testPDF.pdf")


#######################
# class AppURLopener(urllib.request.FancyURLopener):
#     version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'
# urllib._urlopener = AppURLopener()
#
# urllib._urlopener.retrieve('https://onlinelibrary.wiley.com/doi/pdf/10.1002/adma.201706910', "testPDF.pdf")
#######################

##########################################
#
# #Check if folder exists, create if not
# if not os.path.isdir("testPDFs"):
#     os.makedirs("testPDFs")
#
# #cookies
# #cookies = dict(cookies_are = 'working')
#
# f = open('scholar_pdfs.txt')
# allUrls = f.readlines()
# count = 1
#
# for url in allUrls:
#     # url = 'http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.54.9760&rep=rep1&type=pdf'
#     r = requests.get(url, headers = headers)
#     # file = open('testPDF.pdf', 'wb')
#     file = open('testPDFs/%s.pdf' %count, 'wb')
#     file.write(r.content)
#     count+= 1
#
##########################################


# urllib.URLopener.version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'
# filename = 'testPDF.pdf'
#
# filename, headers = urllib.urlretrieve('https://onlinelibrary.wiley.com/doi/pdf/10.1002/adma.201706910')


##########################################################################

# f = open('PDFs/journal.pmed.1001953.pdf', 'rb')
# try:
#     pdf = PdfFileReader(f)
#     info = pdf.getDocumentInfo()
#     if info:
#         print("VALID")
#     else:
#         print("INVALID")
# except Exception as e:
#     print("INVALID")
#
# f.close


#TODO: Delete corrupt PDFs

# for file in os.listdir('PDFs'):
#     if ".DS_Store" not in file:
#         file = 'PDFs/' + file.rstrip()
#         f = open(file, 'rb')
#
#         try:
#             pdf = PdfFileReader(f)
#             info = pdf.getDocumentInfo()
#             if info:
#                 print("VALID")
#             else:
#                 os.remove(file)
#         except Exception as e:
#             os.remove(file)
#
#         f.close


# for file in os.listdir('PDFs'):
#     if ".DS_Store" not in file:
#         f = open('PDFs/%s', file, 'rb')
#         # print(file)


# #Parsing pdf to extract images using pfdminer -> pdf2txt script (MIT License)
# subprocess.run(["python","pdf2txt.py","Wave-of-Wearables.pdf", "--output-dir", "tempImages"])
#
# #Picking one image to save, delete rest
# for file in os.scandir("tempImages"):
#     ext = file.name[-4:].rstrip()
#
#     #size of the biggest file
#     size = 0
#     #path of the biggest file
#     path = ""
#
#     #raw image format, non operable
#     if not ext == ".img":
#         tempPath = file.path
#         tempSize = os.stat(tempPath).st_size
#
#         #Comparing file sizes and identifying path
#         if tempSize > size:
#             size = tempSize
#             path = tempPath.rstrip()
#
# #Copying biggest file to PDFImages dir
# shutil.copy(path, 'PDFImages')
#
#
# print("____________________________")
# print(path)
# print(size)
# print("____________________________")
#
#
#
# #Remove temp dir and its contents
# shutil.rmtree("tempImages")


##########################################
# subprocess.run(["python","pdf2txt.py","PDFs/Increasing_trend_of_wearables_and_multimodalinterface_fo_%20humanactivity.pdf", "--output-dir", "testerImages"])


##########################################

# ###NOTE: START OF CODE BLOCK TO BE COMMITTED TO THE MAIN SCRIPT
#
# #User-Agent Spoofing
# headers = {}
# headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'
#
# driver = webdriver.Chrome('/Users/Arnav/Desktop/Work/chromedriver')
#
# ##### MODIFY 'start' with increments of 10 to go to next page, Pg 1 == 0 #####
# WEBPAGE = 'https://scholar.google.com/scholar?start=80&q=wearables&hl=en&as_sdt=0,22'
#
# driver.get(WEBPAGE)
#
# srcCode = driver.page_source
#
# #<scroll page down snippet>
# last_height = driver.execute_script("return document.body.scrollHeight")
# while True:
#     # Scroll down to the bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     # Wait to load the page
#     time.sleep(2)
#     # Calculate new scroll height and compare with last height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height
#
# driver.quit()
#
#
# #BeautifulSoup instance
# soup = BeautifulSoup(srcCode, 'lxml')
#
# #Saving src code to a text file
# f = open('scholar_src-code.txt', 'w')
# f.write(soup.prettify())
# f.close
#
#
# ## Parsing out
# f = open('TEST.txt', 'w')
#
# # for item in soup.find_all(href = re.compile(".pdf")):
# #     f.write(item.get('href') + "\n")
#
# for item in soup.select('[data-lid]'):
#
#     #Title
#     f.write(item.select('h3')[0].get_text() + "\n")
#
#     #URL
#     f.write('_______________________________________________________________' + "\n")
#     f.write(item.select('a')[0]['href'] + "\n")
#
#     #Synopsis
#     f.write('_______________________________________________________________' + "\n")
#     f.write(item.select('.gs_rs')[0].get_text() + "\n")
#
#
#
#     f.write('_______________________________________________________________' + "\n")
#     f.write('_______________________________________________________________' + "\n")
#     f.write("\n")
#
#
#
# f.close
#
#
# ###NOTE: END OF CODE BLOCK TO BE COMMITTED TO THE MAIN SCRIPT

####
"Extract text, terminal command"

#  pdf2txt.py -o tes.txt PDFs/A-Survey-on-Smart-Wearables-in-the-Application-of-Fitness.pdf

####

####
"Extract metadata from PDF"

# inputPDF = PdfFileReader(open("PDFs/Wearables-in-epilepsy-and-Parkinsons-disease-A-focus-group-study.pdf", "rb"))
# #print(str(inputPDF.getDocumentInfo()))
#
# f = open("metadata.txt", "w")
# f.write(str(inputPDF.getDocumentInfo()))
# f.close

#####


######
#TODO
######

# "Extracting DOI"
#
# inputPDF = "main%20(3).pdf"
# subprocess.run(["python", "pdf2txt.py", "-o", "tes.txt", "PDFs/%s" %inputPDF])
#
# f = open("tes.txt", "r")
# lines = f.readlines()
#
# found = False
# for line in lines:
#     if found == True:
#         break
#     for word in line.split():
#         if "doi" in word:
#             print(line)
#             found = True

######
######


######
#TODO: Parsing Bibtex
######

# f = open("tempBib.txt", "r")
# lines = f.readlines()
#
# for line in lines:
#
#     firstInstance = 0
#     secondInstance = 0
#
#     if line != "\n" and line.rstrip() != "}":
#
#         allKeys = {"doi", "url", "year", "publisher", "author", "title", "booktitle", "journal"}
#         if any(x in line for x in allKeys):
#
#             key = line.split("=")[0].strip()
#             value = line.split("=")[-1].strip()
#
#             #edge case(s)
#             if "booktitle" in key or "journal" in key:
#                 value = value[1:-1]
#             else:
#
#                 #removing certain special characters from string 'value'
#                 specialChars = {"{", "}", ","}
#
#                 for i in specialChars:
#                     value = value.replace(i, '')
#
#
#             # print("Key: %s" %key)
#             # print("Value: %s" %value)
#             print("\n")
#             print("%s: %s" %(key, value))

######
######

dictOfBodyZones = {
    "head": ("head", "helmet", "smart glasses", "make-up"),
    "chest": ("chest", "necklace", "blouse"),
    "back": ("backpack", "jackets"),
    "arms": ("arms", "sleeve", "arm band"),
    "hands+wrist": ("hands+wrist", "glove", "wristbands"),
    "pelvic region": ("pelvic region", "smart underwear", "safety underwear"),
    "legs": ("legs", "tights", "pants", "skirt"),
    "feet": ("feet", "smart shoes", "socks")
}

#testing
for tuple_ in dictOfBodyZones:
    key = tuple_
    value = dictOfBodyZones[key]
    for val in value:
        #%22head%22% +%2B+ %22wearables%22
        val = "%22" + val + "%22" + "+%2B+" + "%22wearables%22"
        print(val)
