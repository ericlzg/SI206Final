import requests
import os
import json
import sqlite3
try:
    import geopandas as gpd
except:
    print("geopandas not installed; installing now... please wait!")
    os.system("conda install geopandas")

APIKEY = "e46386cc5e5e09d97a26eeefbec149181eb9612c"
url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=tract:*&in=state:11&key={APIKEY}"

def getdata():
    response = requests.get(url)
    data = json.loads(response.content)
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
            medianincome = -1
        fips = int(data[i][4])
        cur.execute("INSERT OR IGNORE INTO Tracts (id, name, income, fips_code) VALUES (?,?,?,?)",(i, tractname, medianincome, fips))
        if cur.lastrowid != 0:
            count += 1
    return "All data written"

def modifygeojson(db, infile, outfile):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db)
    cur = conn.cursor() 
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir, infile)
    with open(full_path,'r') as f:
        data = json.load(f)
    for feature in data['features']:
        name = feature['properties']['NAMELSAD']
        cur.execute("SELECT income FROM Tracts WHERE name = ?", (name,))
        rd = cur.fetchall()
        try:
            feature['properties']['INCOME'] = rd[0][0]
        except:
            feature['properties']['INCOME'] = -1
    with open(outfile,'w') as of:
        json.dump(data, of, indent=2)
    return
    




        





    
def main():
    #print(writedb(getdata(),'testdb.db'))
    modifygeojson('testdb.db', "tl_2022_11_tract.geojson", "tracts_with_income.geojson")
main()