#IMPORT NECESSARY LIBRARIES
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
def visualize_boundary(file,ax):
    gdf_boundary=gpd.read_file(file)
    gdf_boundary.plot(ax=ax)

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
    value=sin(latdistance/2)**2+cos(lat1)*cos(lat2)*sin(londistance)
    angular_distance=2*atan2(sqrt(value), sqrt(1-value))
    distance=radius_of_earth*angular_distance
    return distance 


def main():
    cur1, conn1=dom.database_access("sharedfleet.db")
    cur2, conn2=dom.database_access("bus_stops.db")
    geometry_vehicle=point_creater(cur1, "Vehicles")
    geometry_busstop=point_creater(cur2, "bus_stops")
    gdf_vehicle=GeoDataFrame_creation(geometry_vehicle)
    gdf_busstop=GeoDataFrame_creation(geometry_busstop)
    fig, ax = plt.subplots(figsize=[15, 10])
    visualize_boundary("DC.geojson",ax)
    visualize_dots(gdf_busstop, ax, "orange", 5)
    visualize_dots(gdf_vehicle, ax, "red", 20)
    ax.set_xlim(-77.15, -76.90)
    ax.set_ylim(38.79, 39)
    plt.show()

if __name__ == "__main__":
    main()