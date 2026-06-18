
import numpy as np
import geopandas as gpd
from shapely.geometry import Point


# Create points in WGS 84 (lon/lat)
p1 = Point(11.5755, 48.1372) # Munich
p2 = Point(13.0550, 47.8095) # Salzburg

gdf = gpd.GeoDataFrame({'geometry': [p1, p2]}, crs='EPSG:4326')

# 1. Project to a metric CRS (e.g., EPSG:32632 for Southern Germany)
gdf_metric = gdf.to_crs('EPSG:32632')

# 2. Calculate the distance
# gdf_metric.distance(gdf_metric.shift()) will compare row 1 to row 2
distance_meters = gdf_metric.loc[0, 'geometry'].distance(gdf_metric.loc[1, 'geometry'])

print(f"Distance: {distance_meters:.2f} meters")