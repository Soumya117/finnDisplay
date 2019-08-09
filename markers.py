import googlemaps

gmaps = googlemaps.Client(key='google_key')

def getMarkers(address):
    geocode_result = gmaps.geocode(address)
    return geocode_result[0]['geometry']['location']