from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import jsonlines as jl
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb://mongo_db_admin:password@45.76.164.130:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.5.0"
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
    with jl.open(file, "r") as reader:
        for item in reader:
            stats.append(item)
    reader.close()
    return stats

def load_data():
  data = []
  with jl.open("data.jl", "r") as reader:
    for obj in reader:
      data.append(obj)
  reader.close()
  return data[0]

def convert_database():
    database = client.converttest
    users = database.users
    patrols = database.patrols
    radars = database.radars
    kills = database.kills
    disables = database.disables
    sars = database.sars
    global_data = database.global_data
    guilds = load_guilds()
    user_doc, patrol_doc, radar_doc, kill_doc, disable_doc, sar_doc, global_data_doc = [], [], [], [], [], [], []
    for obj in guilds:
        stats = load_stats(obj["file"])
        for item in stats:
          user_doc.append({
            "user_id": item["user"],
            "on_patrol": item["status"][0],
            "on_radar": item["status"][1],
            "cur_patrol": item["cur_patrol"],
            "cur_radar": item["cur_radar"],
            "sar_needed": item["sar_needed"],
            "superuser": item["admin"]
          })
          for patrol in item["patrols"]:
            patrol_doc.append({
              "event_id": patrol["id"],
              "user_id": item["user"],
              "server_id": obj["id"],
              "start": patrol["start"],
              "end": patrol["end"]
            })
          for radar in item["radars"]:
            radar_doc.append({
              "event_id": radar["id"],
              "user_id": item["user"],
              "server_id": obj["id"],
              "start": radar["start"],
              "end": radar["end"]
            })
          for kill in item["kills"]:
            kill_doc.append({
              "event_id": kill["id"],
              "user_id": item["user"],
              "server_id": obj["id"],
              "time": kill["end"]
            })
          for disable in item["disables"]:
            disable_doc.append({
              "event_id": disable["id"],
              "user_id": item["user"],
              "server_id": obj["id"],
              "time": disable["end"]
            })
          for sar in item["sars"]:
            sar_doc.append({
              "event_id": sar["id"],
              "user_id": item["user"],
              "server_id": obj["id"],
              "pilot_id": sar["pilot"],
              "time": sar["end"]
            })
    global_data_doc = load_data()
    if user_doc != []:
      users.insert_many(user_doc)
    if patrol_doc != []:
      patrols.insert_many(patrol_doc)
    if radar_doc != []:
      radars.insert_many(radar_doc)
    if kill_doc != []:
      kills.insert_many(kill_doc)
    if disable_doc != []:
      disables.insert_many(disable_doc)
    if sar_doc != []:
      sars.insert_many(sar_doc)
    global_data.insert_one(global_data_doc)

if __name__ == "__main__":
    convert_database()
