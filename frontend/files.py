import jsonlines
import os
import json

def load_config():
	with open("config.json") as config_file:
		config_data = json.load(config_file)
	return config_data

def load_stats(id):
	#Loads the data from each user from a jsonlines file.
	#Loads every command.
	stats = []
	guild_check = False
	#locates the location of the guilds json
	#by scanning for the file id.
	config_data = load_config()
	database_path = config_data["database_path"]
	with jsonlines.open(f"{database_path}guilds.jl", "r") as reader:
		for obj in reader:
			if obj["id"] == id:
				guild_check = True
				file = obj["file"]
				break
	reader.close()

	if not guild_check:
		return None, 15
	
	#uses the guild filename to load all of the
	#lines for the guild.
	config_data = load_config()
	database_path = config_data["database_path"]

	with jsonlines.open(database_path + file) as reader:
		for obj in reader:
			stats.append(obj)
	reader.close()
	return stats, None

def load_guilds():
	#Loads all the guild files and returns them.
	guilds = []
	config_data = load_config()
	database_path = config_data["database_path"]
	with jsonlines.open(f"{database_path}guilds.jl") as reader:
		for obj in reader:
			guilds.append(obj)
	reader.close()
	return guilds

def load_data():
	#Loads the global data for the bot.
	#Right now only includes the id counter.
	data = []
	config_data = load_config()
	database_path = config_data["database_path"]
	with jsonlines.open(f"{database_path}data.jl") as reader:
		for obj in reader:
			data.append(obj)
	reader.close()
	return data[0]

def save_stats(stats, id):
	#Saves the data after every command is complete.
	#This is so that a bot crash will only result in
	#immediate data loss.

	config_data = load_config()
	database_path = config_data["database_path"]
	#Locates the guild file to be read.
	with jsonlines.open(f"{database_path}guilds.jl", "r") as reader:
		for obj in reader:
			if obj["id"] == id:
				file = database_path + obj["file"]
				break
		reader.close()

	#saves the data in the proper file.
	with jsonlines.open(file, "w") as writer:
		writer.write_all(stats)
	writer.close()

def save_guilds(guilds):
	#Saves the updated guild registry.
	config_data = load_config()
	database_path = config_data["database_path"]
	with jsonlines.open(f"{database_path}guilds.jl", "w") as writer:
		writer.write_all(guilds)
	writer.close()

def save_data(data):
	config_data = load_config()
	database_path = config_data["database_path"]
	#Saves the data in the global data file.
	with jsonlines.open(f"{database_path}data.jl", "w") as writer:
		writer.write(data)
	writer.close()

def create_stats(file):
	#creates the guilds personal file when
	#registering in the registry.
	f = open(file, "x")
	f.close()

def registry_trans():
	pass

def get_id():
	#everytime a new event is created,
	#it is assigned the next id in the
	#positive direction.
	data = load_data()
	data["ids"] += 1
	save_data(data)
	return data["ids"]

def do_register(guildId, guilds):
	guild_check = True
	file = f"{guildId}.jl"
	#scans to make sure the guild has not already
	#been registered.
	for item in guilds:
		if item["id"] == guildId:
			guild_check = False

	if not guild_check:
		return guilds, 9
			
	#if not it adds the entry in the guild
	#registry
	guilds.append({
		"id": guildId,
		"file": file,
		"prefix": "=prime "
	})
	config_data = load_config()
	database_path = config_data["database_path"]
	file = database_path + file
	#creates the guilds registry file.
	if not (os.path.isfile(file) and os.access(file, os.R_OK)):
		create_stats(file)
	return guilds, None