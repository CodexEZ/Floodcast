print("Importing Libraries")

import numpy as np
from pysheds.grid import Grid
import random
import pandas
import geopandas as gpd
import requests
import warnings
from scipy.spatial import ConvexHull
from sklearn.cluster import DBSCAN
from shapely.geometry import Polygon
import time
warnings.filterwarnings("ignore", category=UserWarning)

print("Done ✔")

# Filter specific warning by category
def generate_flood_data():



    url = "https://ffs.india-water.gov.in/ffm/api/station-water-level-above-warning/"
    response = requests.get(url)
    df = pandas.read_csv("D:/Aswin's project/Backend/backend/api/station_map.csv",index_col=False)

    temp_list = []

    if response.status_code == 200 and len(response.json())!=0:
        json_data = response.json()
        for station in json_data:

            row = df[df["Station"]== station["stationCode"]]
            tile = row['Map'].iloc[0]
            print(tile)
            grid = Grid.from_raster(f'D:/Flooding/important/DEMs/{tile}')
            dem = grid.read_raster(f'D:/Flooding/important/DEMs/{tile}')
            inundation = dem < station["value"]
            coords = inundation.coords
            inundation = inundation.flatten()
            inundated_coords = coords[inundation == True]
            sample = np.random.randint(0,len(inundated_coords),1000)
            random_sample = inundated_coords[sample]
            #Now we perform the clustering Algorithms to remove outliers and mark areas
            db = DBSCAN(eps = 0.1,min_samples=5).fit(random_sample)
            labels = db.labels_
            unique_labels = set(labels)

            cluster = random_sample[labels == 0]
            hull = ConvexHull(cluster)

            outline = cluster[hull.vertices]
            #closing the loop
            outline[len(outline)-1] = outline[0]
            poly = Polygon(outline)
            temp_list.append({'name': station["stationCode"],'geometry':poly })
        gdf = gpd.GeoDataFrame(temp_list)
        gdf = gdf.set_geometry('geometry')
        gdf.to_file('bounds.geojson')

    else:
        print("No Rivers above warning level")






print("Generating Flooding data")
start_time = time.time()

generate_flood_data()
end_time = time.time()
print("Done ✔")

print(f"Time elapsed : {end_time - start_time}")
