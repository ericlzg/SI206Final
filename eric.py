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
    for i in range(1,len(data)):
        tract = data[i][0]
        tractname = tract[0: tract.find(";")]
        medianincome = data[i][1]
        fips = data[i][4]



    
def main():
    print('wip')

main()