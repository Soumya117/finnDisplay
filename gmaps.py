# import googlemaps
#
# gmaps = googlemaps.Client(key='AIzaSyBoxlPokqwjkKJPfKNtcXdmbbRuZhp4xjo')
#
# # Geocoding an address
# geocode_result = gmaps.geocode('Solåsveien 20 B, Oslo, Østensjø')
#
# print("GeoCode result: ", geocode_result)

from  geopy.geocoders import Nominatim
geolocator = Nominatim()
city ="London"
country ="Uk"
loc = geolocator.geocode("Rubina Ranas gate 7, Oslo, Gamle Oslo, Norway")
print("latitude is :" ,loc.latitude,"\nlongtitude is:" ,loc.longitude)
