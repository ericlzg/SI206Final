import requests 
import json
import os
import sqlite3
import datetime

#ensure user have geopandas to run the code properly
try:
    import geopandas as gpd
except:
    print("geopandas not installed; installing now... please wait!")
    os.system("conda install geopandas")

#importing libraries for visualization phase
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

#API request to sharedfleet data
def get_data(url): 
    response=requests.get(url)
    data=response.json()
    #To read JSON prettily
    with open("lime_sharedfleet.json","w") as json_file:
        json.dump(data, json_file, indent=4)
    return data

#Set-Up Database
def database_access(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor() 
    return cur, conn

#Type Table
def type_table(data, cur, conn):
    #prepare data
    type_list=[]
    for each in data["data"]["bikes"]:
        vehicle_type = each["vehicle_type"]
        if vehicle_type not in type_list:
            type_list.append(vehicle_type)
    #create table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Types (id INTEGER PRIMARY KEY, type TEXT UNIQUE)"
    )
    #add into database
    for i in range(len(type_list)):
        cur.execute(
            "INSERT OR IGNORE INTO Types (id,type) VALUES (?,?)", (i, type_list[i])
        )
    conn.commit()

#Convert UNIX timestamp into readable format
def unix_conversion(data):
    UNIX_timestamp=data["last_updated"]
    #conversion into readable time
    datetimeobject=datetime.datetime.utcfromtimestamp(UNIX_timestamp)
    #taking time zone into consideration
    EST_timezone = datetime.timezone(datetime.timedelta(hours=-4))
    EST_datetime = datetimeobject.replace(tzinfo=datetime.timezone.utc).astimezone(EST_timezone)
    #formating
    thedatetime = EST_datetime.strftime("%B %d, %Y %I:%M:%S %p GMT-4")
    return thedatetime


#Vehicle Table
def vehicle_table(data, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Vehicles(id INTEGER PRIMARY KEY, vehicle_id TEXT, time TEXT, vehicle_type INTEGER, latitude INTEGER, longitude INTEGER, is_reserved INTEGER, is_disabled INTEGER)")
    #setting up the values 
    count = 0
    cur.execute("SELECT COUNT(*) FROM Vehicles")
    amount= cur.fetchone()[0]
    for i in range(1,len(data["data"]["bikes"])):
        if count >=25 and amount < 1000:
            cur.execute("SELECT COUNT(*) FROM Vehicles")
            amount= cur.fetchone()[0]
            conn.commit()
            return "Limited reached"
        vehicle_id= data["data"]["bikes"][i]["bike_id"]
        #realtime
        time= unix_conversion(data)
        #vehicle_type
        vehicle_type= data["data"]["bikes"][i]["vehicle_type"]
        cur.execute('SELECT id FROM Types WHERE type = ?', (vehicle_type,))
        vehicle_type_id=cur.fetchone()[0]
        #coordinates
        latitude=data["data"]["bikes"][i]["lat"]
        longitude=data["data"]["bikes"][i]["lon"]
        #status
        is_reserved=data["data"]["bikes"][i]["is_reserved"]
        is_disabled=data["data"]["bikes"][i]["is_disabled"]
        #put data into database
        cur.execute("INSERT OR IGNORE INTO Vehicles (id, vehicle_id, time, vehicle_type, latitude, longitude, is_reserved, is_disabled) VALUES (?,?,?,?,?,?,?,?)", (i, vehicle_id, time, vehicle_type_id, latitude, longitude, is_reserved, is_disabled))
        if cur.lastrowid != 0:
            count += 1

    pass

#Status Table
def status_table(cur, conn):
    status_list=["False", "True"]
    cur.execute("CREATE TABLE IF NOT EXISTS Reserved_Disabled(status INTEGER PRIMARY KEY, meaning TEXT)")
    for i in range(len(status_list)):
        cur.execute("INSERT OR IGNORE INTO Reserved_Disabled (status,meaning) VALUES (?,?)", (i, status_list[i]))
    conn.commit()

def main():
    data=get_data("https://data.lime.bike/api/partners/v1/gbfs/washington_dc/free_bike_status.json?")
    cur, conn=database_access("main.db")
    type_table(data, cur, conn)
    unix_conversion(data)
    vehicle_table(data, cur, conn)
    status_table(cur, conn)

if __name__ == "__main__":
    main()