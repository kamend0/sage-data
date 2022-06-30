import pandas as pd
from pymongo import MongoClient
import sys
import urllib.parse
import json

print("Libraries loaded successfully.")

username = "your-username-here"
password = "your-password-here"

CONNECTION_STRING = "mongodb+srv://" + \
                    username + ":" + \
                    password + \
                    "@sage-1.ixupzhc.mongodb.net/?retryWrites=true&w=majority"

# Bring in data in MongoDB-friendly format
try:
    recipes_data = pd.read_json("./raw-data/processed_recipes-data.json")
    print("Recipes loaded successfully.")
except Exception as e:
    print("Some error reading data with Pandas.")
    print(e)
    sys.exit()

recipes_dict = recipes_data.to_dict("records")

print(json.dumps(recipes_dict[:5], indent = 4))

# Make connection to DB
try:
    client = MongoClient(CONNECTION_STRING)
    db = client['recipes-1']
    collection = db['recipes-detail']
    if (collection is not None):
        print("Connection to DB successful.")
except Exception as e:
    print("Something went wrong at the connection level.")
    print(e)
    sys.exit()

# Load data to the DB
try:
    collection.insert_many(recipes_dict)
    print("Load to DB successful. Check MongoDB Atlas.")
except Exception as e:
    print("Something went wrong when loading data to database.")
    print(e)