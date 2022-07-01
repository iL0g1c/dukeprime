from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import jsonlines as jl
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb://mongo_db_admin:{password}@45.76.164.130:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.5.0"
client = MongoClient(connection_string)

def load_guilds():
    guilds = []
    with jl.open(f"guilds.jl", "r") as reader:
        for obj in reader:
            guilds.append(obj)
    reader.close()
    return guilds

def load_stats(file):
    stats = []
    print()
    with jl.open(file, "r") as reader:
        for item in stats:
            stats.append(item)
    reader.close()
    return stats


def convert_database():
    database = client.convertest
    guilds = load_guilds()
    for obj in guilds:
        col = database[str(obj["file"])]
        
        stats = load_stats(obj["file"])
        x = col.insert_many(stats)

if __name__ == "__main__":
    convert_database()
