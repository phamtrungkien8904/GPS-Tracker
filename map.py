# pip install contextily geopandas shapely
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
from shapely.geometry import Point
from pyproj import Transformer
from matplotlib.ticker import MaxNLocator, FuncFormatter

# Hanoi Center Coordinates
lat, lon = 21.0285, 105.8542  

# 2. Create a GeoDataFrame for the point (Contextily uses Web Mercator projection)
gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs="EPSG:4326")
gdf = gdf.to_crs(epsg=3857)  # Convert to standard web map projection

# 3. Initialize Matplotlib plot
fig, ax = plt.subplots(figsize=(8, 8), dpi=100)

transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

# 4. Set map boundaries (buffer size determines how much of the block is seen)
buffer = 1000  # meters around the point
ax.set_xlim(gdf.geometry.x.iloc[0] - buffer, gdf.geometry.x.iloc[0] + buffer)
ax.set_ylim(gdf.geometry.y.iloc[0] - buffer, gdf.geometry.y.iloc[0] + buffer)

# 5. Add the OpenStreetMap background tiles
zoom = 17
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=zoom)

# Show coordinate ticks in longitude/latitude while keeping the map in Web Mercator.
ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
ax.yaxis.set_major_locator(MaxNLocator(nbins=5))

def format_lon(x, _pos):
	lon, _lat = transformer.transform(x, gdf.geometry.y.iloc[0])
	return f"{lon:.5f}"


def format_lat(y, _pos):
	_lon, lat = transformer.transform(gdf.geometry.x.iloc[0], y)
	return f"{lat:.5f}"


ax.xaxis.set_major_formatter(FuncFormatter(format_lon))
ax.yaxis.set_major_formatter(FuncFormatter(format_lat))

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.savefig("map.png", dpi=300, bbox_inches="tight")
plt.show()