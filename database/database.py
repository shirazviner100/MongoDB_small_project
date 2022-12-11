from pymongo import MongoClient
import ssl

#Mongo detailed
MONGO_URI = "mongodb+srv://shiraz:1234@clustersv.hm43ohg.mongodb.net/test"
client = MongoClient(MONGO_URI, ssl_cert_reqs = ssl.CERT_NONE)
db = client.SV

#collections initialize
users_col = db.get_collection("users")
products_col = db.get_collection("products")
orders_col = db.get_collection("orders")


