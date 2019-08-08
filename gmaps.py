import googlemaps

gmaps = googlemaps.Client(key='')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

print("GeoCode result: ", geocode_result[0]['geometry']['location'])
