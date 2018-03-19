#!/usr/bin/env python

"""A tool used for uploading data to the db backend for govpulse."""

# MONGODB
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.congressional_record

# UTILITIES
from datetime import datetime, date


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

    """from stackoverflow"""


# PROCESSORS

"""Processes the json input file (expects input in the form of the congressional
record json parser) and uploads it in a more reusable format to the central
database."""


def process_speeches(data):
    location = {
        "volume": data["header"]["vol"],
        "number": data["header"]["num"],
        "chamber": data["header"]["chamber"],
        "pages": data["header"]["pages"],
        "extension": data["header"]["extension"]
    }
    date = datetime.strptime(data["header"]["month"] + data["header"]["day"] + data["header"]["year"], "%B%d%Y")
    title = data["title"]
    id = data["id"]

    items = []

    for record in data["content"]:
        # filter out items that are not substantive or not made by a member of congress
        if record["kind"] == "speech" and record["speaker_bioguide"] is not None:
            items.append({
                "text": record["text"][len(record["speaker"]) + 4:].replace(" \n", " ").replace("\n  ", "\n\t").replace(
                    "\n\n\n", " "),
                "speaker": record["speaker"],
                "speaker_id": record["speaker_bioguide"],
                "location": location,
                "date": date,
                "title": title,
                "document_id": id,
                "id": id + ":" + str(record["itemno"])
            })

    return items


# COMMAND LINE HANDLING

import argparse
import json
import traceback

parser = argparse.ArgumentParser()
parser.add_argument("type", help="the type of data to upload", choices=["speeches"])
parser.add_argument("files", nargs='+', metavar='FILE', help="the location of the file to process")
args = parser.parse_args()

for file in args.files:
    try:
        with open(file, "r") as infile:
            data = json.load(infile)

        print("Loaded " + file)

        if args.type == "speeches":
            to_add = process_speeches(data)
            print("Inserting %s new records..." % str(len(to_add)))
            db.speeches.insert_many(to_add)
    except Exception as e:
        traceback.print_exc()
