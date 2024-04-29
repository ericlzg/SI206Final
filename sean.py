import matplotlib.pyplot as plt
import os
import sqlite3
import requests

# Define the API endpoint URL
url = "https://api.wmata.com/Bus.svc/json/jStops"

# Set up the request headers with your API key
headers = {
    "api_key": "26315e26b1c74e1e9489fb9b79b9678a"  # Replace "YOUR_API_KEY" with your actual WMATA API key
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the JSON response data
    data = response.json()
    # Extract and print the latitude and longitude of each bus stop
    for stop in data['Stops']:
        stop_id = stop['StopID']
        lat = stop['Lat']
        lon = stop['Lon']
        name = stop['Name']
        # print(f"Stop ID: {stop_id}, Latitude: {lat}, Longitude: {lon}, Name: {name}")
else:
    # Print an error message if the request failed
    print("Failed to fetch bus stops. Status code:", response.status_code)
    
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

# Function to create GeoDataFrame for bus stops
def create_geo_dataframe(data):
    geometry = [Point(float(stop['Lon']), float(stop['Lat'])) for stop in data['Stops']]
    gdf_bus_stops = gpd.GeoDataFrame(data['Stops'], geometry=geometry, crs="EPSG:4326")
    return gdf_bus_stops

# Function to plot bus stops on Matplotlib axis
def visualize_bus_stops(gdf_bus_stops, ax):
    gdf_bus_stops.plot(marker='o', color='red', markersize=5, ax=ax)

# Plot the bus stops
def plot_bus_stops(data):
    # Create GeoDataFrame for bus stops
    gdf_bus_stops = create_geo_dataframe(data)
    
    # Plot bus stops
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf_bus_stops.plot(ax=ax)
    
    # Set axis labels
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    
    # Show plot
    plt.show()

# Plot the bus stops
plot_bus_stops(data)