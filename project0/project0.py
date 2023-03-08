import re
import sqlite3
import requests
from typing import List
from io import BytesIO
import PyPDF4
# from PyPDF4 import PdfFileReader



def fetchincidents(url:str)->bytes:
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"                          
    response = requests.get(url, headers=headers)
    binary_data = response.content
    return binary_data

def extractincidents(binary_data)->List[list[str]]:
    pdfreader = PyPDF4.PdfFileReader(BytesIO(binary_data))
    totalnumberofpages = pdfreader.getNumPages()

    p1 = '^\d{1,2}\/\d{1,2}\/\d{1,4}\s(?:[01]\d|2[0-3]):(?:[0-5]\d)$'  
    p2 = '^\d{1,4}(?:-\d{1,8})?$'                              
    p5 = '^(EMSSTAT|\d{5}|OK\d{7})$' 

    data = []            
    ls = [None] * 5  
    k = 0     

    for pagenum in range(totalnumberofpages):
        page = pdfreader.getPage(pagenum).extractText().split("\n")[:-1]
        for line in page:
            if re.match(p1, line):
                ls[0] = line
            elif re.match(p2, line):
                ls[1] = line
            elif re.match(p5, line):
                ls[4] = line
                data.append(ls)
                ls = [None] * 5
                k = 0
            elif k < 2:
                if ls[2] is None:
                    ls[2] = line
                    k += 1
                elif ls[3] is None:
                    ls[3] = line
                    k += 1
            else:
                ls[2] += ls[3]
                ls[3] = line

    return data

def createdb():
    connection = sqlite3.connect('normanpd.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS incidents (
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT
    )''')
    connection.commit()
    return connection

def populatedb(db, data):
    with db:
        cur = db.cursor()
        cur.executemany("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)", data)
        db.commit()

        #cur.execute("SELECT * FROM incidents")
        #rows = cur.fetchall()
        #for row in rows:
           # print(row)

def status(db):
    cursor = db.cursor()
    cursor.execute('''
        SELECT nature, COUNT(*) as count
        FROM incidents
        GROUP BY nature
        ORDER BY count DESC, nature
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(f"{row[0]}|{row[1]}")
    db.commit()
    db.close()