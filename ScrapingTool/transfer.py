from selenium import webdriver
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
import sys
import config
import csv
#SQL
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine


#DB
cnx = mysql.connector.connect(
host = config.host,
user = config.user,
password = config.passwd,
port = config.port)

print(cnx)
readCursor = cnx.cursor(buffered = True)
writeCursor = cnx.cursor(buffered = True)
db_name = config.db_name

# Read from matrix + Write to MAIN
query = "SELECT * FROM scholardb.matrix"
readCursor.execute(query)


doi = "doi_placeholder"
journal = "journal_placeholder"

f = open('matrixdb__.csv', 'r')
allLines = f.readlines()
i = 0

for(pic_id, reference_name, reference_link, fabrications, body_zones, materials, functions, year, conference_venue, website, authors) in readCursor:

    doi = allLines[i]
    i = i + 1

    print(doi.rstrip() + " " + reference_link + " " + year + " " + conference_venue + " " + authors + " " + reference_name + " " + "journal_placeholder" + " " + fabrications + " " + body_zones + " " + materials + " " + functions + "\n")
    writeCursor.execute(
        "INSERT INTO scholardb.MAIN (doi, url, year, publisher, authors, title, journal, fabrications, body_zones, materials, functions) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(doi.strip(), reference_link.strip(), year.strip(), conference_venue.strip(), authors.strip(), reference_name.strip(), journal.strip(), fabrications.strip(), body_zones.strip(), materials.strip(), functions.strip()))

#Create images table
# readCursor.execute("CREATE TABLE images (doi VARCHAR(255), images VARBINARY(MAX))")



cnx.commit()
readCursor.close()
writeCursor.close()
cnx.close()
