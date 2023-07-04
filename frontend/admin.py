from files import load_guilds, save_guilds

def do_cradmin(stats, user):
	user_check = False
	for item in stats:
		if item["user"] == user:
			user_check = True
			item["admin"] = True
			return stats, None
	
	if not user_check:
		return stats, 3

def do_remev(stats, event_id, user):
	admin_check = False
	valid_id = False
	for item in stats:
		if item["user"] == user and item["admin"]:
			admin_check = True
			
	for item in stats:
		for patrol in item["patrols"]:
			if patrol["id"] == int(event_id):
				valid_id = True
				if item["status"][0] == "online":
					item["status"][0] = "offline"
					item["cur_patrol"] = None
				del item["patrols"][item["patrols"].index(patrol)]
		for radar in item["radars"]:
			valid_id = True
			if item["status"][1] == "online":
				item["status"][1] = "offline"
				item["cur_radar"] = None
			del item["radars"][item["radars"].index(radar)]
		for kill in item["kills"]:
			if kill["id"] == int(event_id):
				valid_id = True
				del item["kills"][item["kills"].index(kill)]
		for disable in item["disables"]:
			if kill["id"] == int(event_id):
				valid_id = True
				del item["disables"][item["disables"].index(disable)]
		for sar in item["sars"]:
			if kill["id"] == int(event_id):
				valid_id = True
				del item["sars"][item["sars"].index(sar)]
	if not valid_id:
		return stats, 14
	elif not admin_check:
		return stats, 17
	return stats, None

def do_prefix(stats, token, user, id):
	admin_check = False
	guild_check = False
	
	guilds = load_guilds()
	for item in stats:
		if item["user"] == user and item["admin"]:
			admin_check = True
	for guild in guilds:
		if guild["id"] == id:
			guild_check = True
			guilds[guilds.index(guild)]["prefix"] = token
	if not admin_check:
		return 17
	if not guild_check:
		return 15
	save_guilds(guilds)
	return None

def load_prefix(bot, message):
	guilds = load_guilds()
	for guild in guilds:
		if guild["id"] == message.guild.id:
			return guild["prefix"]
	return "=prime "