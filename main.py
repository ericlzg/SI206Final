try:
    import geopandas as gpd
except:
    print("geopandas not installed; installing now... please wait!")
    os.system("pip install geopandas")
import os
import sqlite3
import requests

APIKEY = "e46386cc5e5e09d97a26eeefbec149181eb9612c"
url = f"https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=tract:*&in=state:11&key={APIKEY}"

def pulldata(url):
    response = requests.get(url)
    return response

def writeintodb(data,db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    


def main():
    print('wip')

main()