#!/usr/bin/env python3

from __future__ import annotations
import os, csv, sys, asyncio, time, re
from pathlib import Path
from collections import defaultdict
from enum import Enum, auto

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
import folium


_DATASET_ENDPOINT = Path(os.getcwd()).resolve()
REGION = ["Sumatera", "Jawa", "Kalimantan", "Sulawesi", "Nusa Tenggara", "Maluku", "Papua"]


def indonesia_geolocation(dpath: str, fname: str) -> None:
   frame = defaultdict(list,{ k:[] for k in ('Istance', 'Location', 'Latitude','Longitude') })
   dt = pd.read_csv(_DATASET_ENDPOINT / f'datasets/{dpath}.csv')

   for value in dt['Instance']:
      with Nominatim(user_agent="indonesia_geolocator") as geolocator:
         try:
            location = geolocator.geocode(f"{value}")
            if location is not None:
               addr = location.address
               lat = location.latitude
               long = location.longitude
         
               frame['University'].append(value)
               frame['Location'].append(addr)
               frame['Latitude'].append(lat)
               frame['Longitude'].append(long)
         except GeocoderUnavailable:
            print("Geocoder service is unavailable. Retrying in 5 seconds...")
            time.sleep(5)
            return indonesia_geolocation()
         except Exception as e:
            print(f"{value} - An unexpected error occurred: {e}")
            continue
   
   df = pd.DataFrame(frame)
   with open(f'{fname}.csv', 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(list(frame.keys()))
      
      for i in range(len(df)):
         row = [df[column_name][i] for column_name in list(frame.keys())]
         writer.writerow(row)

   print(f"CSV file '{fname}.csv' has been created with the output.")
         

def find_island(location):
    for region in REGION:
        if re.search(region, location, re.IGNORECASE):
            return region
    return None

def map_helper(dpath: str) -> None:

   dt = pd.read_csv(f'{dpath}.csv')
   dt['Island'] = dt['Location'].apply(find_island)
   maps = folium.Map(location=[-2.5489, 118.0149], zoom_start=5)

   color_mapping = {
      'Sumatera': 'red',
      'Jawa': 'blue',
      'Kalimantan': 'green',
      'Sulawesi': 'orange',
      'Nusa Tenggara': 'purple',
      'Maluku': 'darkred',
      'Papua': 'lightblue'
   }
   for index, row in dt.iterrows():
      island = row['Island']
      exact_color = color_mapping.get(island, 'gray')
      folium.Circle(location=[row['Latitude'], row['Longitude']],
                     radius = 50000,
                     color = exact_color,
                     fill_color = exact_color,
                     tooltip=f"{row['University']}",
                  ).add_to(maps)

   # Save the map as an HTML file
   maps.save('university_locations.html')