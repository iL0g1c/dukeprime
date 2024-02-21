from datetime import datetime

from files import get_id

def do_kill(user, date_amount, time_amount, stats):
	user_check = False
	#scans for the currect user.
	for item in stats:
		if item["user"] == user:
			user_check = True
			#adds an entry log for the kill
			id = get_id()
			item["kills"].append({
				"id": id,
				"end": str(datetime.combine(date_amount, time_amount))
			})
			#retrieves the number of kills and
			#disables.
			kills = len(item["kills"])
			disables = len(item["disables"])
			event_id = id
			return stats, kills, disables, event_id, None
	if not user_check:
		return stats, None, None, None, 3

def do_disable(user, date_amount, time_amount, stats):
	user_check = False
	#locates the correct user json.
	for item in stats:
		if item["user"] == user:
			user_check = True
			#does the same thing as for kills.
			id = get_id()
			item["disables"].append({
				"id": id,
				"end": str(datetime.combine(date_amount, time_amount))
			})
			kills = len(item["kills"])
			disables = len(item["disables"])
			return stats, kills, disables, id, None
	return stats, None, None, None, 3