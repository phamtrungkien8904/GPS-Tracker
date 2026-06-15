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
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon

# Custom settings
plt.style.use('classic')
plt.rcParams.update({
    'figure.dpi': 100,
    'figure.figsize': (10, 8),
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.linewidth': 2,
    'axes.labelsize': 15,
    'axes.labelcolor': 'black',
    'savefig.facecolor': 'white',
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial'],
    'mathtext.fontset': 'cm',

    'savefig.bbox': 'tight',
    # Ticks
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.major.size": 8,
    "ytick.major.size": 8,
    "xtick.major.width": 2,
    "ytick.major.width": 2,
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "xtick.minor.size": 4,
    "ytick.minor.size": 4,
    "xtick.minor.width": 1.5,
    "ytick.minor.width": 1.5,
})

inch = 2.54  # cm per inch

# Hanoi Center Coordinates
lat_0, lon_0 = 21.0285, 105.8542  
# lat_0, lon_0 = 48.137154, 11.576124  # Munich Center Coordinates

buffer_x = 1000000  # meters around the point
buffer_y = 1000000  # meters around the point




data = np.genfromtxt("GPS.dat", delimiter=",", skip_header=1, dtype=str)  # Load your data as strings first
GPS_time = np.array([np.datetime64(t) for t in data[:, 0]])  # Convert timestamp strings to datetime
GPS_lat = data[:, 1].astype(float)   # Assuming the second column is latitude
GPS_lon = data[:, 2].astype(float)   # Assuming the third column is longitude

print("GPS Time:", GPS_time)




# 2. Create a GeoDataFrame for the point (Contextily uses Web Mercator projection)
gdf = gpd.GeoDataFrame(geometry=[Point(lon_0, lat_0)], crs="EPSG:4326")
gdf = gdf.to_crs(epsg=3857)  # Convert to standard web map projection

# 3. Initialize Matplotlib plot

fig, ax = plt.subplots()
ax.set_aspect('equal')


transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)


# 4. Set map boundaries (buffer size determines how much of the block is seen)

ax.set_xlim(gdf.geometry.x.iloc[0] - buffer_x, gdf.geometry.x.iloc[0] + buffer_x)
ax.set_ylim(gdf.geometry.y.iloc[0] - buffer_y, gdf.geometry.y.iloc[0] + buffer_y)

# 5. Add the OpenStreetMap background tiles
zoom = 6
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

# scalebar = AnchoredSizeBar(
# 	ax.transData,
# 	buffer_x/2,
# 	f"{buffer_x/2:.0f} m",
# 	"lower right",
# 	pad=0.5,
# 	color="black",
# 	frameon=False,
# 	size_vertical=20,
# 	fontproperties=fm.FontProperties(size=10),
# )
# ax.add_artist(scalebar)

# Plot GPS track/points if data was loaded
gps_gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(GPS_lon, GPS_lat), crs="EPSG:4326")
gps_gdf = gps_gdf.to_crs(epsg=3857)
# Plot line connecting points
ax.plot(gps_gdf.geometry.x, gps_gdf.geometry.y, color="red", linewidth=1, label="GPS Track")
# Plot points
ax.scatter(gps_gdf.geometry.x, gps_gdf.geometry.y, color="red", s=20)


def add_fancy_scalebar(ax, length, location,
                       height, linewidth,
                       text_offset):
    """
    length: total scale bar length in map units (meters)
    location: axes fraction coordinates (x,y)
    """

    # Convert axes fraction to data coordinates
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    x0 = xlim[0] + location[0] * (xlim[1] - xlim[0])
    y0 = ylim[0] + location[1] * (ylim[1] - ylim[0])

    segment = length / 2

    # Left segment (black)
    ax.add_patch(Rectangle(
        (x0, y0),
        segment,
        height,
        facecolor='black',
        edgecolor='black',
        linewidth=linewidth,
        zorder=100
    ))

    # Right segment (white)
    ax.add_patch(Rectangle(
        (x0 + segment, y0),
        segment,
        height,
        facecolor='white',
        edgecolor='black',
        linewidth=linewidth,
        zorder=100
    ))

    # Labels
    ax.text(x0, y0 - text_offset, "0",
            ha='center', va='top', fontsize=10)

    ax.text(x0 + segment, y0 - text_offset,
            f"{segment/1000:g}",
            ha='center', va='top', fontsize=10)

    ax.text(x0 + length, y0 - text_offset,
            f"{length/1000:g}",
            ha='center', va='top', fontsize=10)

    ax.text(x0 + segment, y0 + 3*text_offset,
            "km",
            ha='center', va='top', fontsize=10)

add_fancy_scalebar(
    ax,
    length=buffer_x/2,  # 10 km total
    location=(0.72, 0.05),
    height=buffer_y/50,  # 1% of the y-range
    linewidth=1.5,
    text_offset=buffer_y/50  # 2% of the y-range
)



ax.legend()

plt.savefig("map.png", bbox_inches="tight")
plt.show()