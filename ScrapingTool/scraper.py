from bs4 import BeautifulSoup
import requests
import re
import pdfminer
import os
import subprocess
import urllib.request
import certifi
import urllib3
# urllib3.disable_warnings()

#http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

#def pdfLinks(href):
    #return href and re.compile(".pdf").search(href)

#If files exist already, delete
files = ["scholar_src-code.txt", "scholar_pdfs.txt"]
for f in files:
    if os.path.exists(f):
        os.remove(f)
    else:
        print("File '%s' does not exist." %f)

try:
    pageAddress = 'https://scholar.google.com/scholar?start=0&q=wearables&hl=en&as_sdt=0,22'

    #User-Agent Spoofing
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'

    #Getting html data (src code)
    response = requests.get(pageAddress, headers = headers)

    #Status code
    print("Status Code:", response.status_code)

    #BeautifulSoup instance
    soup = BeautifulSoup(response.content, 'lxml')

    #Saving src code to a text file
    f = open('scholar_src-code.txt', 'w')
    f.write(soup.prettify())
    f.close

    #Parsing out pdf links and writing them to scholar_pdfs.txt
    f = open('scholar_pdfs.txt', 'w')

    for item in soup.find_all(href = re.compile(".pdf")):
        f.write(item.get('href') + "\n")

    f.close

    #TODO:Read URLs from scholar_pdfs.txt and save PDF files in a folder

    #Check if folder exists, create if not
    if not os.path.isdir("PDFs"):
        os.makedirs("PDFs")

    f = open('scholar_pdfs.txt', 'r')
    allUrls = f.readlines()

    count = 1



    # for url in allUrls:
    #     #urllib.request takes in url and saves output in specified file
    #     try:
    #         urllib.request.urlretrieve(url, "PDFs/%s.pdf" %count)
    #     except urllib.error.HTTPError as exception
    #         continue
    #     count += 1

    #testing
    # urllib.request.urlretrieve('https://www.researchgate.net/profile/Ella_Dagan/publication/333938009_Design_Framework_for_Social_Wearables/links/5d1a8938299bf1547c8f77f9/Design-Framework-for-Social-Wearables.pdf', "PDFs/test.pdf")



    # for url in allUrls:
    #     r = requests.get(url, headers = headers)
    #     file = open('PDFs/%s.pdf' %count, 'wb')
    #     file.write(r.content)
    #     count += 1

    #TODO: Urllib unable to access blocked URLs, handle errors

    #testing
    r = requests.get('https://www.researchgate.net/profile/Ella_Dagan/publication/333938009_Design_Framework_for_Social_Wearables/links/5d1a8938299bf1547c8f77f9/Design-Framework-for-Social-Wearables.pdf', headers = headers)
    file = open('PDFs/test.pdf', 'wb')
    file.write(r.content)


    #Parsing pdf to extract images using pfdminer -> pdf2txt script (MIT License)
    #subprocess.run(["python","pdf2txt.py","test.pdf", "--output-dir", "test"])

except Exception as e:
    print(str(e))

#pdfminer.pdf2text()
