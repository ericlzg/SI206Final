#IMPORT NECESSARY LIBRARIES
import json
import dom 
from shapely.geometry import Point
import os
try:
    import geopandas as gpd
except:
    print("geopandas not installed; installing now... please wait!")
    os.system("conda install geopandas")
import geopandas as gpd
import matplotlib.pyplot as plt

import subprocess
try:
    import mapclassify
except ImportError:
    subprocess.check_call(['pip', 'install', '--upgrade', 'mapclassify'])
    import mapclassify

from math import radians, sin, cos, sqrt, atan2



#SET-UP
#function that pulls lon and lat from a database table into a coordinate form
def coordinate(cur, table_name):
    cur.execute(f'SELECT longitude, latitude FROM {table_name}')
    coordinates=cur.fetchall()
    return coordinates

#1ST VISUALIZATION
#function that convert coordinates into plottable points
def point_creater(cur, table_name):
    geometry=[]
    for each in coordinate(cur, table_name):
        point=Point(each[0], each[1])
        geometry.append(point) 
    return geometry

#function that creates the GeoDataFrame for plotting purposes
def GeoDataFrame_creation(geometry):
    gdf_dict={'geometry':geometry}
    gdf_object=gpd.GeoDataFrame(gdf_dict, geometry='geometry', crs="EPSG:4326")
    return gdf_object

#function that plot the base map
def visualize_census(file,ax):
    gdf_boundary=gpd.read_file(file)
    gdf_boundary.plot(column="INCOME", ax=ax, scheme="equal_interval", edgecolor="k", legend=True)

#function that plot in dots form
def visualize_dots(gdf_object, ax, color, markersize):
    gdf_object.plot(marker='o', color=color, markersize=markersize, ax=ax)

#
#
#

#2ND VISUALIZATION
#function that takes two coordinates and measure the distance between them in kilometers (using Haversine Formula)
def calc_distance(coordinate1, coordinate2):
    #conversion to radians
    lon1 = radians(coordinate1[0])
    lat1 = radians(coordinate1[1])
    lon2 = radians(coordinate2[0])
    lat2 = radians(coordinate2[1])
    #distance between lon&lat
    londistance=lon2-lon1
    latdistance=lat2-lat1
    #Haversine formula
    radius_of_earth=6371
    value=sin(latdistance/2)**2+cos(lat1)*cos(lat2)*sin(londistance/2)**2
    angular_distance=2*atan2(sqrt(value), sqrt(1-value))
    distance=radius_of_earth*angular_distance
    return distance 

def dist_from_tract(infile, tractname, db1, db2, outfile):
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir, infile)
    with open(full_path,'r') as f:
        data = json.load(f)


def main():
    cur1, conn1=dom.database_access("main.db")
    cur2, conn2=dom.database_access("main.db")
    cur3, conn3=dom.database_access("main.db")

    geometry_vehicle=point_creater(cur1, "Vehicles")
    geometry_busstop=point_creater(cur2, "bus_stops")
    gdf_vehicle=GeoDataFrame_creation(geometry_vehicle)
    gdf_busstop=GeoDataFrame_creation(geometry_busstop)

    #visualization 1
    fig1, ax1 = plt.subplots(figsize=[15, 10])
    visualize_dots(gdf_vehicle, ax1, "red", 2)
    ax1.set_xlim(-77.15, -76.90)
    ax1.set_ylim(38.79, 39)
    ax1.set_xlabel("longitude")
    ax1.set_ylabel("latitude")
    ax1.set_title("Sharedfleet (Lime) in Washington DC")

    #visualization 3
    fig3, ax3 = plt.subplots(figsize=[15, 10])
    visualize_census("tracts_with_income.geojson", ax3)
    visualize_dots(gdf_busstop, ax3, "cyan", 3)
    visualize_dots(gdf_vehicle, ax3, "red", 2)
    ax3.set_xlim(-77.15, -76.90)
    ax3.set_ylim(38.79, 39)
    ax3.set_xlabel("longitude")
    ax3.set_ylabel("latitude")
    ax3.set_title("Overlay of Sharefleet and Bus Stops over Census Tract in Washington DC")
    plt.show()

if __name__ == "__main__":
    main()

    #print(calc_distance((38.911534,-77.04167), (38.916999,-77.027574)))