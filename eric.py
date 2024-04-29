import requests
import os
import sqlite3

APIKEY = "e46386cc5e5e09d97a26eeefbec149181eb9612c"
url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=tract:*&in=state:11&key={APIKEY}"

def getdata():
    data = requests.get(url)
    return data

def writedb(data,db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db)
    cur = conn.cursor() 
    cur.execute("CREATE TABLE IF NOT EXISTS Tracts (id INTEGER PRIMARY KEY, name TEXT UNIQUE, income INTEGER, fips_code INTEGER)")
    count = 0
    for i in range(1,len(data)):
        if count >= 25:
            conn.commit()
            return "Terminating after reaching write limit"
        tract = data[i][0]
        tractname = tract[0: tract.find(";")]
        medianincome = int(data[i][1])
        if medianincome < 0:
            medianincome = None
        fips = int(data[i][4])
        cur.execute("INSERT OR IGNORE INTO Tracts (id, name, income, fips_code) VALUES (?,?,?,?)",(i, tractname, medianincome, fips))
        if cur.lastrowid != 0:
            count += 1
    return "All data written"
        





    
def main():
    print('wip')

main()