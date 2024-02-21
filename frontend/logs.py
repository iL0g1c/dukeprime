from files import load_config
import csv

def write_log(event_id, time_stamp, guild_id, user_id, action):
	config_data = load_config()
	database_path = config_data["database_path"]
	with open(f"{database_path}log.csv", "a") as f:
		writer = csv.writer(f)
		writer.writerow((event_id, time_stamp, guild_id, user_id, action))
	f.close()