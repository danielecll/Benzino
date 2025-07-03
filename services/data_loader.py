import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
from sklearn.neighbors import BallTree



DATA = {}
TREE = None
PLACE_IDS = []
COORDS = []

def deg2rad(degrees):
    return np.radians(degrees)

def check(path: str):
    if not os.path.exists(path):
        update()
        return

    mod_time = os.path.getmtime(path)
    mod_datetime = datetime.fromtimestamp(mod_time)
    now = datetime.now()

    if now - mod_datetime >= timedelta(hours=24):
        print("The file has NOT been modified in the last 24 hours. Updating...")
        update()

def update():
    urlprice = "https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv"
    urlanagrafico = "https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv"

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
            continue

    json.dump(data, open("data/merged.json", "w"))

def load_data():
    global DATA, TREE, PLACE_IDS, COORDS


    check("data/merged.json")

    with open("data/merged.json", "r") as f:
        DATA = json.load(f)

    PLACE_IDS.clear()
    COORDS.clear()

    for pid, values in DATA.items():
        try:
            lat = float(values.get('lat'))
            lon = float(values.get('lon'))
            if not np.isnan(lat) and not np.isnan(lon):
                PLACE_IDS.append(pid)
                COORDS.append([lat, lon])
        except:
            continue

    coords_rad = np.radians(COORDS)
    TREE = BallTree(coords_rad, metric='haversine')

    print("TREE initialized...")