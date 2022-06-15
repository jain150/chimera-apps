import pandas as pd
import config
import csv

#SQL
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine


#creates db
def create_database(cursor, database):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

#def insert_entry():
	#TODO

def main():

    cnx = mysql.connector.connect(
    host = config.host,
    user = config.user,
    password = config.passwd,
    port = config.port)



    print(cnx)
    cursor = cnx.cursor(buffered = True)

    db_name = config.db_name



    try:
        cursor.execute("USE {}".format(db_name))

        #TODO: Create Table
        # cursor.execute("CREATE TABLE bibtex (doi VARCHAR(255), url VARCHAR(255), year VARCHAR(255), publisher VARCHAR(255), author VARCHAR(255), title VARCHAR(255), booktitle VARCHAR(255))")
        #TODO: Insert data to table
        # cursor.execute("INSERT INTO bibtex (doi, url, year, publisher, author, title, booktitle) VALUES ('test', '242', '33333', '4', '4', '5', '69')")
        # cursor.execute("SELECT * FROM bibtex")

        ###TODO:Add Matrix DB to Main DB###

        df = pd.read_csv('newMatrixDB.csv')
        df = df.fillna('')
        df = df.astype(str)
        # print("%s  %s  %s  %s  %s  %s  %s" %(df['PIC ID'][0].strip(), df['Reference Name'][0].strip(), df['Reference Link'][0].strip(), df['Year'][0].strip(), df['Conference (VENUE)'][0].strip(), df['Website'][0].strip(), df['AUTHORS'][0].strip()))

        #Create new table
        # cursor.execute("CREATE TABLE matrix (pic_id VARCHAR(255), reference_name VARCHAR(255), reference_link VARCHAR(255), fabrications VARCHAR(255), body_zones VARCHAR(255), materials VARCHAR(255), functions  VARCHAR(255), year VARCHAR(255), conference_venue VARCHAR(255), website VARCHAR(255), authors VARCHAR(255))")
        #Insert single entry
        # entry = "INSERT INTO matrix (pic_id, reference_name, reference_link, fabrications, body_zones, materials, functions, year, conference_venue, website, authors) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(df['PIC ID'][1].replace("'", "-").strip(), df['Reference Name'][1].replace("'", "-").strip(), df['Reference Link'][1].replace("'", "-").strip(), df['Fabrications'][1].replace("'", "-").strip(), df['Body Zones'][1].replace("'", "-").strip(), df['Materials'][1].replace("'", "-").strip(), df['Functions'][1].replace("'", "-").strip(), df['Year'][1].replace("'", "-").strip(), df['Conference (VENUE)'][1].replace("'", "-").strip(), df['Website'][1].replace("'", "-").strip(), df['AUTHORS'][1].replace("'", "-").strip())
        # print(entry)
        # cursor.execute(entry)

        for i in df.index:
        	cursor.execute(
                "INSERT INTO scholardb.matrix (pic_id, reference_name, reference_link, fabrications, body_zones, materials, functions, year, conference_venue, website, authors) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(df['PIC ID'][i].replace("'", "-").strip(), df['Reference Name'][i].replace("'", "-").strip(), df['Reference Link'][i].replace("'", "-").strip(), df['Fabrications'][i].replace("'", "-").strip(), df['Body Zones'][i].replace("'", "-").strip(), df['Materials'][i].replace("'", "-").strip(), df['Functions'][i].replace("'", "-").strip(), df['Year'][i].replace("'", "-").strip(), df['Conference (VENUE)'][i].replace("'", "-").strip(), df['Website'][i].replace("'", "-").strip(), df['AUTHORS'][i].replace("'", "-").strip()))

        cursor.execute("SELECT * FROM matrix")


        print(cursor.fetchall())
    except mysql.connector.Error as err:
        print("Database {} does not exist.".format(db_name))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor, db_name)
            print("Database {} created successfully.".format(db_name))
            cnx.database = db_name
        else:
            print(err)
            exit(1)

    cnx.commit()
    cursor.close()
    cnx.close()

if __name__ == "__main__":
	main()
