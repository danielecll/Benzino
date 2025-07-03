import numpy as np
import services.data_loader as data_loader 

def locate_stations(rdata):
    print("TREE in locate_stations:", data_loader.TREE)
    my_location_rad = np.radians([rdata.lat, rdata.lon])
    radius_rad = rdata.radius / 6371

    indices, _ = data_loader.TREE.query_radius([my_location_rad], r=radius_rad, sort_results=True, return_distance=True)

    nearest = [data_loader.DATA[data_loader.PLACE_IDS[i]] for i in indices[0]]
    cheapest = sorted(
        [x for x in nearest if rdata.fuel in x],
        key=lambda x: float(x[rdata.fuel])
    )

    return {"n": nearest, "c": cheapest}