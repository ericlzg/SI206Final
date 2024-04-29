import matplotlib.pyplot as plt
import os
import sqlite3
import requests
import geopandas as gpd
from shapely.geometry import Point

# Define the API endpoint URL
url = "https://api.wmata.com/Bus.svc/json/jStops"

# Set up the request headers with your API key
headers = {
    "api_key": "26315e26b1c74e1e9489fb9b79b9678a"  # Replace "YOUR_API_KEY" with your actual WMATA API key
}

# Function to fetch bus stop data from the API
def get_bus_stop_data(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch bus stops. Status code:", response.status_code)
        return None

# Function to create SQLite database for bus stops
def create_bus_stop_database(data, db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Create bus stops table
    cur.execute('''CREATE TABLE IF NOT EXISTS bus_stops (
                    stop_id TEXT PRIMARY KEY,
                    latitude REAL,
                    longitude REAL
                    )''')

    # Insert data into bus stops table
    for stop in data['Stops']:
        stop_id = stop['StopID']
        lat = stop['Lat']
        lon = stop['Lon']
        cur.execute("INSERT OR IGNORE INTO bus_stops (stop_id, latitude, longitude) VALUES (?, ?, ?)", (stop_id, lat, lon))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Function to retrieve bus stop data from the database
def retrieve_bus_stop_data(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # Retrieve bus stop data from the database
    cur.execute("SELECT * FROM bus_stops")
    rows = cur.fetchall()

    # Close connection
    conn.close()

    return rows

# Function to create GeoDataFrame for bus stops from database
def create_geo_dataframe_from_db(db_name):
    # Retrieve bus stop data from the database
    rows = retrieve_bus_stop_data(db_name)

    # Create GeoDataFrame
    geometry = [Point(lon, lat) for _, lat, lon in rows]
    gdf_bus_stops = gpd.GeoDataFrame(geometry=geometry, columns=['geometry'], crs="EPSG:4326")

    return gdf_bus_stops

# Function to plot bus stops from database
def plot_bus_stops_from_db(db_name):
    # Create GeoDataFrame for bus stops
    gdf_bus_stops = create_geo_dataframe_from_db(db_name)
    
    # Plot bus stops
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf_bus_stops.plot(ax=ax, color='green', markersize=2)
    
    # Set axis labels
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    
    # Show plot
    plt.show()

def main():
    # Fetch bus stop data
    data = get_bus_stop_data(url, headers)
    if data:
        # Create SQLite database for bus stops
        create_bus_stop_database(data, "bus_stops.db")
        print("Bus stop data successfully saved to database.")

        # Plot bus stops from database
        plot_bus_stops_from_db("bus_stops.db")
    else:
        print("Failed to save bus stop data to database.")

if __name__ == "__main__":
    main()
