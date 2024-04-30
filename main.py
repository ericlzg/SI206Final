import os
try:
    import geopandas as gpd
except:
    print("geopandas not installed; installing now... please wait!")
    os.system("conda install geopandas")
import sqlite3
import requests
import json
import datetime
import dom
import eric
import sean
