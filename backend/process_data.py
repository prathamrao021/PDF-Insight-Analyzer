import urllib.request
from pypdf import PdfReader
import pandas as pd
import re
import sqlite3
import argparse
import os
import glob

def fetchincidents(pdf):
    reader = PdfReader(pdf)
    data = ''
    for page in reader.pages:
        data = data + "\n" + page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False)

    return data


def extractincidents(data):

    lines = (data.split("\n"))[4:-1]
    rows = []

    temp_row = []
    temp_text = ""
    for line in lines:
        split_line = [field.strip() for field in line.split("          ") if field.strip()]

        if len(split_line) < 5:
            if len(temp_row) > 0:
                temp_row[2] += " " + split_line[0]
                
        else:
            if len(temp_row) == 5:
                temp_text += "\t".join(temp_row)
                temp_text += "\n"
                rows.append(temp_row)
            temp_row = split_line 

    if len(temp_row) == 5:
        rows.append(temp_row)
        temp_text += "\t".join(temp_row)


    with open('resources/data.tsv','a') as file:
        file.write(temp_text)
    
    return rows
    
def main_workflow():
    pdf_files = glob.glob(os.path.join('uploads', '*.pdf'))

    for pdf_file in pdf_files:
        incidents = fetchincidents(pdf_file)
        separated_data = extractincidents(incidents)

    

# if __name__ == "__main__":
#     main_workflow()













# def createdb():
#     if os.path.exists("resources/normanpd.db"):
#         os.remove("resources/normanpd.db")
#     conn = sqlite3.connect("resources/normanpd.db")
    
#     cursor = conn.cursor()
    
#     cursor.execute("CREATE TABLE IF NOT EXISTS incidents (incident_time TEXT, incident_number TEXT, incident_location TEXT, nature TEXT, incident_ori TEXT)")
    
#     conn.commit()
#     conn.close()


# def populatedb(separated_data):
#     conn = sqlite3.connect("resources/normanpd.db")
    
#     cursor = conn.cursor()
    
#     cursor.executemany("INSERT INTO incidents VALUES(?, ?, ?, ?, ?)", separated_data)
#     conn.commit()
#     conn.close()

# def status():
#     conn = sqlite3.connect("resources/normanpd.db")
    
#     cursor = conn.cursor()
    
#     cursor.execute("SELECT nature, count(nature) FROM incidents GROUP BY nature ORDER BY nature ASC")
#     printables = cursor.fetchall()
#     data = ''
#     with open("resources/status.txt", "w") as file:
#         for i,v in enumerate(printables):
#             if v[0] == "Nature":
#                 continue
#             if i != len(printables) - 1:
#                 file.write(f"{v[0]}|{v[1]}\n")
#                 data += f"{v[0]}|{v[1]}\n"
#             else:
#                 file.write(f"{v[0]}|{v[1]}")
#                 data += f"{v[0]}|{v[1]}"
#     conn.close()
#     print(data)
#     return data

# if __name__ == "__main__":
    
    
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--incidents", type=str, required=True, help="Incident summary url.")
#     args = parser.parse_args()
    
#     filename = downloaddata(args.incidents)
#     data = fetchincidents("resources/incident1.pdf")
#     separated_data = extractincidents(data)
#     createdb()
#     populatedb(separated_data[1:])
#     status()
    
    