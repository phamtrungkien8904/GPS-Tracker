# pip install contextily geopandas shapely matplotlib-map-utils
import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
from shapely.geometry import Point
from pyproj import Transformer
from matplotlib.ticker import MaxNLocator, FuncFormatter
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm

# Hanoi Center Coordinates
lat_0, lon_0 = 21.0285, 105.8542  




data = np.genfromtxt("GPS.dat", delimiter=",", skip_header=1, dtype=str)  # Load your data as strings first
GPS_time = np.array([np.datetime64(t) for t in data[:, 0]])  # Convert timestamp strings to datetime
GPS_lat = data[:, 1].astype(float)   # Assuming the second column is latitude
GPS_lon = data[:, 2].astype(float)   # Assuming the third column is longitude

print("GPS Time:", GPS_time)




# 2. Create a GeoDataFrame for the point (Contextily uses Web Mercator projection)
gdf = gpd.GeoDataFrame(geometry=[Point(lon_0, lat_0)], crs="EPSG:4326")
gdf = gdf.to_crs(epsg=3857)  # Convert to standard web map projection

# 3. Initialize Matplotlib plot
fig, ax = plt.subplots(figsize=(6, 6), dpi=80)


transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)


# 4. Set map boundaries (buffer size determines how much of the block is seen)
buffer = 1000  # meters around the point
ax.set_xlim(gdf.geometry.x.iloc[0] - buffer, gdf.geometry.x.iloc[0] + buffer)
ax.set_ylim(gdf.geometry.y.iloc[0] - buffer, gdf.geometry.y.iloc[0] + buffer)

# 5. Add the OpenStreetMap background tiles
zoom = 14
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

scalebar = AnchoredSizeBar(
	ax.transData,
	buffer/5,
	f"{buffer/5:.0f} m",
	"lower right",
	pad=0.5,
	color="black",
	frameon=False,
	size_vertical=10,
	fontproperties=fm.FontProperties(size=10),
)
ax.add_artist(scalebar)

# Plot GPS track/points if data was loaded
gps_gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(GPS_lon, GPS_lat), crs="EPSG:4326")
gps_gdf = gps_gdf.to_crs(epsg=3857)
# Plot line connecting points
ax.plot(gps_gdf.geometry.x, gps_gdf.geometry.y, color="red", linewidth=1, label="GPS Track")
# Plot points
ax.scatter(gps_gdf.geometry.x, gps_gdf.geometry.y, color="red", s=20)
ax.legend()



plt.savefig("map.png", bbox_inches="tight")
plt.show()