import IP2Location

# Open the downloaded BIN database file
database = IP2Location.IP2Location("IP2LOCATION-LITE-DB11.IPV6.BIN")

# Perform the lookup
ip_address = "209.85.220.41"
rec = database.get_all(ip_address)

# Output results
print(f"IP Address: {ip_address}")
print(f"Country: {rec.country_long}")
print(f"Region: {rec.region}")
print(f"City: {rec.city}")
print(f"Latitude: {rec.latitude}")
print(f"Longitude: {rec.longitude}")
print(f"Time Zone: GMT{rec.timezone}")
print(f"ZIP Code: {rec.zipcode}")

# Always close the database handler
database.close()