#!/usr/bin/env python

"""Initializes the database running on the local machine (accessible via localhost) on port 27017 so that it's
ready to handle govpulse data. This script will create all necessary indexes, unique keys, etc."""

import pymongo

print(__doc__)
client = pymongo.MongoClient("mongodb://localhost:27017")

# initialize CONGRESSIONAL_RECORD
db = client.congressional_record
db.speeches.drop_indexes()
db.speeches.create_index("id", unique=True)
db.speeches.create_index([("text", pymongo.TEXT)], unique=False, default_language='english')

# initialize LEGISLATORS
db = client.legislators
db.congress.drop_indexes()
db.congress.create_index("id", unique=True)

print("...done.")
