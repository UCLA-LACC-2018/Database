import pymongo
from pymongo import MongoClient
import json

# Create a MongoClient to interact with MongoDB Service
client = MongoClient()

# Choose a database
db = client.test_database

import requests

map_url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.712800,-74.006000&radius=10&type=hotels&keyord=stay&key=AIzaSyBZrFa436xs5vDPP5hswpA7RfM02K6MIdQ"
map_response = requests.get(map_url)
map_results = json.loads(map_response.text)["results"]

hotels = db.hotels
hotels.insert_many(map_results)

least = hotels.find().sort([("rating",-1)]).limit(1)
print(least[0]["name"])

best = hotels.find().sort([("rating",+1)]).limit(1)
print(least[0]["name"])

cursor = hotels.find()
for doc in cursor:
    loc = doc["geometry"]["location"]
    lat = loc["lat"]
    lon = loc["lng"]
    print(loc)
    weather_url = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lon) + "&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
    weather_response = requests.get(weather_url)
    weather_results = json.loads(weather_response.text)["main"]["temp"]
    print(doc["name"])
    print(weather_results)


#
# print(weather_results)

# for doc in cursor:
#     print(doc)
#
#collection.insert_many(results)

# collection.ensure_index([('rating',pymongo.ASCENDING)] )
#collection.ensure_index([('rating',pymongo.DESCENDING)] )
#cursor=collection.find().sort([("rating",-1)]).limit(1)
# cursor=collection.find()
# for doc in cursor:
#     print(doc["name"])
#
#print(results)
#collection.insert_many(j["results"])

