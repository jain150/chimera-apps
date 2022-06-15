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
cursor = cnx.cursor(buffered = True)
db_name = config.db_name



f = open('classiDB.csv', 'r')
allLines = f.readlines()

for line in allLines:
    tokens = line.split(',')
    DOI = tokens[0]
    tutorial = tokens[1]
    research = tokens[2]
    designConcepts = tokens[3]
    patents = tokens[4]
    aestheticApproach = tokens[5]
    classification = ""


    if "x" in tutorial:
        classification += "++Tutorial"

    if "x" in research:
        classification += "++Research"

    if "x" in designConcepts:
        classification += "++Design Concepts"

    if "x" in patents:
        classification += "++Patents"

    if "x" in aestheticApproach:
        classification += "++Aesthetic Approach"


    # print("DOI -> %s\n" %DOI)
    # print("Classification -> %s\n" %classification)
    # print("\n")

    cursor.execute(
        "UPDATE scholardb.MAIN SET classification = '%s' WHERE doi = '%s'" %(classification, DOI))

cnx.commit()
cursor.close()
cnx.close()
