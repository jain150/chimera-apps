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
# AWS
import boto3

#DB
cnx = mysql.connector.connect(
host = config.host,
user = config.user,
password = config.passwd,
port = config.port)

print(cnx)
cursor = cnx.cursor(buffered = True)
db_name = config.db_name

if not os.path.exists('AllPDFsWithNoImages.txt'):
    f = open('AllPDFsWithNoImages.txt', 'w')
    f.write("***FOLLOWING IS A LIST OF PDFs THAT DID NOT RETURN ANY IMAGES***" + "\n" + "\n")
    f.close

if not os.path.exists('bibTexData.csv'):
    f = open('bibTexData.csv', 'w')
    f.write("doi,url,year,publisher,author,title,booktitle/journal")
    f.close

dictOfFunctions = {
    "aesthetics": ("aesthetics, artistic", "beauty", "art"),
    "breathability": ("breathability"),
    "cognitive": ("cognitive", "emotion", "reaction", "mental", "imagination"),
    "control": ("control", "command"),
    "display": ("display", "screen", "highlight"),
    "electronics connections": ("electronics connections", "contact", "conductivity", "bonds", "link"),
    "emissivity": ("emissivity", "glow", "radiation"),
    "energy harvesting": ("energy harvesting", "solar panels", "static energy"),
    "feedback": ("feedback", "haptic", "olfactory", "visual", "tactile"),
    "gestures" : ("gestures", "pinch", "turn", "grasp", "grab", "flick"),
    "interactions": ("interactions", "touch", "press", "hold", "move", "swipe", "scroll"),
    "interfaces": ("interfaces"),
    "modularity": ("modularity", "parts", "models", "templates", "patterns"),
    "morphology": ("morphology", "change shape", "structure"),
    "movement": ("movement", "dynamic"),
    "protective": ("protective", "security", "isolation", "insultation"),
    "sensing": ("sensing", "capacitive", "humidity", "light", "temperature", "force", "pressure"),
    "skins": ("skins"),
    "storage": ("storage", "data", "physical"),
    "studies": ("studies", "reviews", "surveys", "application", "inquiries"),
    "wireless communication": ("wireless communication", "wifi", "bluetooth", "radio frequency", "rfid")
}

# TODO: complete the following two dicts:
dictOfFabrications = {
    "3D printing": ("3D printing", "digital fabrication"),
    "embroidery+applique": ("embroidery+applique", "embellishment", "needlepoint", "beading"),
    "heat transfer": ("heat transfer", "vacuum forming", "pressing"),
    "knit": ("knit", "interlink", "knot", "crochet", "lace"),
    "laser cutting": ("laser cutting", "digial fabrication"),
    "layering": ("layering", "coating"),
    "machining": ("machining", "lathe", "table saw"),
    "molding+casting": ("molding+casting", "sand molding", "shell mold"),
    "origami": ("origami"),
    "painting": ("painting", "spray", "traditional"),
    "pleating+folding": ("pleating+folding"),
    "printing": ("printing", "screen printing", "inkjet printing"),
    "soldering": ("soldering"),
    "sticking": ("sticking", "join", "hold", "glue", "attach"),
    "stitching+sewing": ("stitching+sewing"),
    "weaving": ("weaving", "interlacing")

}

dictOfMaterials = {
    "Adhesives": (),
    "Conductive Inks": (),
    "Conductive Threads": (),
    "Electronics": (),
    "Hardware": (),
    "Illumination": (),
    "Metal": (),
    "Molding Materials": (),
    "Organic Materials": (),
    "Paper and Cardboard": (),
    "Polymers": (),
    "Regular Inks": (),
    "Shape Memory Alloy": (),
    "Textile+Composites": (),
    "Threads": ()
}

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

#creates db
def create_database(cursor, database):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

## Checks for corrupts PDF files and deletes them, returns True if corrupt
def corruptPDF(filename, dirPath):
    file = dirPath + '/' + filename.rstrip()
    f = open(file, 'rb')

    try:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        if info:
            print("PDF " + "\"" + filename.rstrip() + "\"" + " PASSES THE CHECK" + "\n")
        else:
            os.remove(file)
            return True

    except Exception as e:
        os.remove(file)
        return True
    f.close

# try:

cursor.execute("USE {}".format(db_name))
#Create table
# cursor.execute("CREATE TABLE MAIN (doi VARCHAR(255), url VARCHAR(255), year VARCHAR(255), publisher VARCHAR(255), authors VARCHAR(255), title VARCHAR(255), journal VARCHAR(255), fabrications VARCHAR(255), body_zones VARCHAR(255), materials VARCHAR(255), functions  VARCHAR(255))")
#doi -> doi; url -> reference_link; year -> year; publisher -> conference_venue; authors -> authors; title -> reference_name; booktitle/journal -> journal


#Taking console input -> 'search keyword'
# keyword = sys.argv[1]

category = sys.argv[1]
mainKey = sys.argv[2]
#value = [sys.argv[3]]
#pgNumber = (int(sys.argv[4]) - 1) * 10

#To run: python crawler.py <category> <elements> <example> <pageNumber>. Eg. 'python crawler.py bz head glasses 1'

## SAVING IMAGES

#Check if folder exists, create if not; Final Images saved here
if not os.path.isdir("PDFImages"):
    os.makedirs("PDFImages")

for f in os.scandir("PDFs"):

    # print("__________________________________________________________________________________________________________________________________")
    # print(f.path)
    # print("__________________________________________________________________________________________________________________________________")

    try:
        print("try2")
        #Parsing pdf to extract images using pfdminer -> pdf2txt script (MIT License)
        subprocess.run(["python","pdf2txt.py", f.path, "--output-dir", "tempImages"])
        print("try2end")
    except Exception as e:
        print("except2")
        print(str(e))

    #Picking one image to save, delete rest

    #size of the biggest file
    size = 0
    #path of the biggest file
    path = ""
    #number of iterations; to verify if we're dealing w/ a single image; no comparison
    numIter = 0

    tempPath = ""
    #preserving extension of the selected image
    selectedExt = ""

    #number of .jpg file occurences
    numJPG = 0

    for file in os.scandir("tempImages"):
        ext = file.name[-4:].rstrip()

        #raw image format (.img), non operable
        if not ext == '.img':
            #at least one operable image exists
            numIter += 1

            if ext == '.jpg':
                numJPG += 1

                tempPath = file.path
                #selected image file size
                tempSize = os.stat(tempPath).st_size

                #Comparing file sizes and identifying path
                if tempSize > size:
                    size = tempSize
                    selectedExt = ext
                    path = tempPath.rstrip()

    #Second loop to handle non .jpg files
    for file in os.scandir("tempImages"):
        ext = file.name[-4:].rstrip()

        #At least one image exists, no .jpg files were procured
        if numIter > 0 and numJPG == 0:

            tempPath = file.path
            #selected image file size
            tempSize = os.stat(tempPath).st_size

            #Comparing file sizes and identifying path
            if tempSize > size:
                size = tempSize
                selectedExt = ext
                path = tempPath.rstrip()


    #sole image in the folder
    if(numIter == 1):
        path = tempPath

    if(numIter > 0):

        #Renaming the biggest file to its PDF name

        #removing trailing '.pdf' and adding original ext using 'Python negative slicing'
        tempStr = f.name.rstrip()[:-4] + selectedExt

        #destPath = "PDFs/%s" %tempStr
        destPath = "tempImages/%s" %tempStr

        os.rename(path, destPath)

        #Copying file to PDFImages dir
        shutil.copy(destPath, 'PDFImages')

        #Remove temp dir and its contents
        shutil.rmtree("tempImages")

    #No images retrieved
    else:
        #List of PDFs where images weren't retrived for whatever reasons
        f_ = open('AllPDFsWithNoImages.txt', 'a')
        f_.write(f.name)

        #Add generic image to the PDFImages folder instead; rename it to the corresponding PDF first
        print("FAILED: NO IMAGES WERE EXTRACTED FOR PDF FILE: %s" %f)

        #IDEA: Maybe instead of this implementation, just link one generic
        #image to all the ones that don't have a corresponding image in the DB

        #Making a copy of 'genericImage' in the PDFIMages folder
        shutil.copy('genericImage.jpg', 'PDFImages')

        tempStr = f.name.rstrip()[:-4] + ".jpg"

        initialPath = "PDFImages/genericImage.jpg"
        destPath = "PDFImages/%s" %tempStr
        #Renaming the generic Image to correspond to the PDF
        os.rename(initialPath, destPath)


## EXTRACTING BIBTEX AND FURTHER PARSING

for pdf in os.scandir("PDFs"):

    #print(pdf)
    if corruptPDF(pdf.name, 'PDFs'):
        continue

    subprocess.run(["python", "pdf2txt.py", "-o", "tempDOI.txt", pdf.path])

    f = open("tempDOI.txt", "r")
    lines = f.readlines()

    bibtexRaw = None
    incomplete = False
    DOI = None
    doiFound = False

    #iterate thru each line; obtain DOI
    for line in lines:
        # print("\nLINE ----------------------> " + line)
        if line != "\n" or not line:
            #doi incomplete; trailing to next line
            if incomplete:
                DOI = DOI + line.split()[0]
                #DOI = DOI.strip('.')
                incomplete = False

            #iterate thru each word
            for word in line.split():
                if "doi." in word:

                    print("\nWORD ------------------>" + word)


                    try:
                        DOI = line.split("org/")[1]
                        DOI = DOI.rstrip("\n")
                        DOI = DOI.replace(")", "")
                        DOI = DOI.strip('.')
                        #Extracting BibTex to test
                        bibtexRaw = subprocess.run(["doi2bib", DOI], stdout = subprocess.PIPE)
                        print("DOI ----->" + DOI)
                        print("bibtex ----->" + bibtexRaw.stdout.decode())
                        # print("DOI ------------> " + DOI)
                        #checking if DOI is complete; bibtex would be empty or 'false'
                        if not bool(bibtexRaw.stdout):
                            incomplete = True
                        else:
                            doiFound = True
                            break

                    except Exception as e:
                        print("DOI parse ERROR: %s" %e)


        if(doiFound):
            print(DOI)
            break
    ##Extracting bibtex data, final
    #bibtexRaw = subprocess.run(["doi2bib", DOI], stdout = subprocess.PIPE)

    #Writing bibtex data to file
    f = open('tempBib.txt', 'w')
    # print(bibtexRaw.stdout) #testing
    if(bibtexRaw is None):
        break
    f.write(bibtexRaw.stdout.decode())
    f.close

    file_name = pdf.path.strip('.pdf')
    file_name = file_name.replace('PDFs', 'PDFImages')
    print("DOI -->> %s" %DOI)
    print(file_name)
    image_name = "%s.jpg" % file_name


    #Setting up the S3 client; Secret Access Key (not to be shared, only kept on the local computer)
    s3 = boto3.resource('s3',
        aws_access_key_id="AKIAQW755M3D4EKRRH3W",
        aws_secret_access_key="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"
    )

    #renaming the filename as the corresponding DOI (+ ext) and pushing the image to the AWS S3 bucket
    try:
        if(bibtexRaw is not None):
            s3.meta.client.upload_file(image_name, 'chimeraimages', "%s.jpg" % DOI.strip())
    except Exception as e:
        print("S3 UPLOAD ERROR: %s" %e)


    ## PARSING bibtex data stored in 'tempBib.txt'
    ## SAVING TO .csv

    f_ = open('bibTexData.csv', 'a')
    f_.write("\n")

    f = open("tempBib.txt", "r")
    lines = f.readlines()


    doi = ""
    url = ""
    year = ""
    publisher = ""
    authors = ""
    title = ""
    journal = ""
    fabrications = ""
    body_zones = ""
    materials = ""
    functions = ""

    for line in lines:

        firstInstance = 0
        secondInstance = 0

        # cursor.execute("CREATE TABLE MAIN (doi VARCHAR(255), url VARCHAR(255), year VARCHAR(255), publisher VARCHAR(255), authors VARCHAR(255), title VARCHAR(255), journal VARCHAR(255), fabrications VARCHAR(255), body_zones VARCHAR(255), materials VARCHAR(255), functions  VARCHAR(255))")
        #doi -> doi; url -> reference_link; year -> year; publisher -> conference_venue; authors -> authors; title -> reference_name; booktitle/journal -> journal

        if line != "\n" and line.rstrip() != "}":

            allKeys = {"doi", "url", "year", "publisher", "author", "title", "booktitle", "journal"}
            if any(x in line for x in allKeys):

                key = line.split("=")[0].strip()
                value = line.split("=")[-1].strip()

                #edge case(s)
                if "booktitle" in key or "journal" in key:
                    value = value[1:-1]
                else:

                    #removing certain special characters from string 'value'
                    specialChars = {"{", "}", ","}

                    for i in specialChars:
                        value = value.replace(i, '')

                if("booktitle" in key or "journal" in key):
                    journal = value
                elif("doi" in key):
                    doi = value
                elif("url" in key):
                    url = value
                elif("year" in key):
                    year = value
                elif("publisher" in key):
                    publisher = value
                elif("author" in key):
                    authors = value
                elif("title" in key):
                    title = value

                if category == "fb":
                    fabrications = mainKey
                elif category == "bz":
                    body_zones = mainKey
                elif category == "mt":
                    materials = mainKey
                elif category == "fn":
                    functions = mainKey
                else:
                    print("Incorrect category type. Please enter 'fb, bz, mt, fn'")
                    continue

                    #Test: saving 'elements' and not 'examples' here (taxonomy)
                    # body_zones = key

    try:
        if(bibtexRaw is not None):
            cursor.execute(
                "INSERT INTO scholardb.MAIN (doi, url, year, publisher, authors, title, journal, fabrications, body_zones, materials, functions) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(doi.strip(), url.strip(), year.strip(), publisher.strip(), authors.strip(), title.strip(), journal.strip(), fabrications.strip(), body_zones.strip(), materials.strip(), functions.strip()))
    except Exception as e:
        print("DB PUSH ERROR: %s" %e)

#Resetting back to state 0, avoiding dupes
shutil.rmtree("PDFImages")


cnx.commit()
cursor.close()
cnx.close()
