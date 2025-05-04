import os
import time
from datetime import datetime, timedelta
import json
import pandas as pd # type: ignore
import numpy as np
from sklearn.neighbors import BallTree

def deg2rad(degrees):
    return np.radians(degrees)

def check(path: str):
    mod_time = os.path.getmtime(path)
    mod_datetime = datetime.fromtimestamp(mod_time)
    now = datetime.now()
    if now - mod_datetime < timedelta(hours=24):
        print("The file has been modified in the last 24 hours. Skipping update")
        return
    else: 
        print("The file has NOT been modified in the last 24 hours. Updating...")
        update()

def update():
    urlprice = "url"
    urlanagrafico = "url


    dfa = pd.read_csv(urlanagrafico, skiprows=1, sep=";", on_bad_lines='warn')
    data = {}
    for _, row in dfa.iterrows():
        data[row["idImpianto"]] = {
            "address": str(row["Indirizzo"]) + " " + str(row["Comune"]),
            "name": row["Bandiera"],
            "lat": row["Latitudine"],
            "lon": row["Longitudine"]
            }

    df = pd.read_csv(urlprice, skiprows=1, sep=";", on_bad_lines='warn')
    for _, row in df.iterrows():
        try:
            data[row["idImpianto"]][row["descCarburante"]] = row["prezzo"]
            data[row["idImpianto"]]["Self"] = row["isSelf"]
        except:
            pass

    json.dump(data, open("merged.json", "w+"))


check("merged.json")


def locate(location: list, radius):
    data = json.load(open("merged.json", "r"))

    my_location_rad = deg2rad(location)

    place_ids = []
    coordinates = []

    for place_id, values in data.items():
        lat = values.get('lat')
        lon = values.get('lon')

        try:
            lat = float(lat)
            lon = float(lon)

            if np.isnan(lat) or np.isnan(lon):
                raise ValueError("NaN detected")

            place_ids.append(place_id)
            coordinates.append([lat, lon])

        except (TypeError, ValueError):
            pass

    coords_rad = np.radians(coordinates)
    tree = BallTree(coords_rad, metric='haversine')
    radius_rad = radius / 6371

    indices = tree.query_radius([my_location_rad], r=radius_rad)

    nearest = []

    for idx in indices[0]:
        nearest.append(data[place_ids[idx]])
    return nearest


nearest = locate([41.816739, 12.654046], 1)
print(nearest)


'''
s = 100
address = ""
name = ""
for _id in data:
    try:
        b = data[_id]["Gasolio"]
        if b < s:
            s = b
            address = data[_id]["address"]
            name = data[_id]["name"]
    except Exception as e:
        print(e)

print(s)
print(address)
print(name)

place_name = "Lazio"

# Scarica tutti i punti di interesse che sono stazioni di benzina
tags = {'amenity': 'fuel'}
gdf = ox.features_from_place(place_name, tags=tags)

# Esporta i dati in CSV
gdf.to_csv("fuel_stations_italy.csv")

# Carica il CSV (assicurati di sostituire il nome del file con quello che hai)
df = pd.read_csv('fuel_stations_italy.csv')

# Crea una mappa centrata sull'Italia
mappa = folium.Map(location=[41.9028, 12.4964], zoom_start=6)  # Latitudine e longitudine di Roma

def reverse_geocode(lat, lon):
    geolocator = Nominatim(user_agent="reverselocationfinder")
    location = geolocator.reverse((lat, lon), language='it')
    
    if location:
        return location.address
    else:
        return "Address not found"


# Aggiungi i punti delle stazioni di benzina sulla mappa
for _, row in df.iterrows():
    s = row['geometry'].split(" ")
    s[1] = s[1].replace("(", "")
    lon = float(s[1].replace(",", ""))
    s[2] = s[2].replace(")", "")
    lat = float(s[2].replace(",", ""))
    
    print(reverse_geocode(lat, lon))

    folium.Marker(
        location=[s[2], s[1]],
        popup=row['name']  # Nome della stazione (opzionale)
        ).add_to(mappa)

# Salva la mappa come HTML
mappa.save('stazioni_benzina_italia.html')

# Stampa un messaggio di successo
print("Mappa salvata come 'stazioni_benzina_italia.html'")
'''
