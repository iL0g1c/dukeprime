from datetime import timedelta, datetime
from files import get_id

def round_delta(obj):
	secs = round(obj.total_seconds())
	return timedelta(seconds=secs)

def round_seconds(obj):
	obj_date = obj.date()
	if type(obj) is datetime:
		obj = obj.time()
	if obj.microsecond >= 500_000:
		obj = datetime.combine(obj_date, obj) + timedelta(seconds=1)

	output = obj.replace(microsecond=0)
	if not (type(obj) is datetime):
		output = datetime.combine(obj_date, output)
	
	return output

def get_total_patrols(patrols, user):
	#cycles through all of the users.
	#and finds the correct user.
	total = timedelta(seconds=0)
	for patrol in patrols:
		if patrol["user"] == user:

			#scans through all of the patrols,
			#and extracts all of the times and,
			#then totals them all up.
			start = datetime.strptime(patrol["start"], "%Y-%m-%d %H:%M:%S.%f")
			end = datetime.strptime(patrol["end"], "%Y-%m-%d %H:%M:%S.%f")
			duration = end - start
			total += duration
	return round_delta(total)

def log_on(user, date_amount, time_amount, status, stats):
	start_check = False
	user_check = False
	#scans for the right user.
	for item in stats:
		if item["user"] == user:
			user_check = True
			if item["status"][0] == "offline":
				start_check = True
				id = get_id()
				cur_patrol = id
				start = datetime.combine(date_amount, time_amount)
				stats[stats.index(item)]["status"][0] = status
				stats[stats.index(item)]["cur_patrol"] = cur_patrol
				stats[stats.index(item)]["patrols"].append({
					"id": id,
					"start": str(start),
					"end": None
				})
				return stats, id, None
	if not user_check:
		stats.append({
			"user": user,
			"status": ["offline", "offline"],
			"cur_patrol": None,
			"cur_radar": None,
			"kills": [],
			"disables": [],
			"sar_needed": "no",
			"patrols": [],
			"radars": [],
			"sars": [],
			"admin": False
		})
		return log_on(user, date_amount, time_amount, status, stats)
	elif not start_check:
		return stats, None, 1

def radar_on(user, date_amount, time_amount, status, stats):
	start_check = False
	user_check = False
	#scans for the right user.
	for item in stats:
		if item["user"] == user:
			user_check = True
			if item["status"][1] == "offline":
				start_check = True
				id = get_id()
				cur_patrol = id
				start = datetime.combine(date_amount, time_amount)
				stats[stats.index(item)]["status"][1] = status
				stats[stats.index(item)]["cur_radar"] = cur_patrol
				stats[stats.index(item)]["radars"].append({
					"id": id,
					"start": str(start),
					"end": None
				})
				return stats, id, None
	if not user_check:
		stats.append({
			"user": user,
			"status": ["offline", "offline"],
			"cur_patrol": None,
			"cur_radar": None,
			"kills": [],
			"disables": [],
			"sar_needed": "no",
			"patrols": [],
			"radars": [],
			"sars": [],
			"admin": False
		})
		return radar_on(user, date_amount, time_amount, status, stats)
	elif not start_check:
		return stats, None, 1

def log_off(user, date_amount, time_amount, status, stats):
	start_check = False
	user_check = False
	#identifies the valid online user.
	patrols = []
	for item in stats:
		if item["user"] == user:
			user_check = True
			if item["status"][0] == "online":
				start_check = True
				for patrol in item["patrols"]:
					#scans for the unclosed patrol
					#splices in the end timestamp.
					if patrol["id"] == item["cur_patrol"]:
						start = patrol["start"]
						start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
						end = datetime.combine(date_amount, time_amount)
						patrol["end"] = str(end)
						event_id = patrol["id"]
						start = round_seconds(start)
						end = round_seconds(end)
					patrol["user"] = item["user"]
					patrols.append(patrol)

				total_patrols = get_total_patrols(patrols, item["user"])
				#calculates the length of the patrol
				duration = end - start
				stats[stats.index(item)]["status"][0] = status
				stats[stats.index(item)]["cur_patrol"] = None
				return stats, duration, len(item["patrols"]), total_patrols, event_id, None

	if not user_check:
		return stats, None, None, None, None, 3
	elif not start_check:
		return stats, None, None, None, None, 2

def confirm_patrol(stats, user_id):
	for user in stats:
		if user_id == user["user"]:
			if user["cur_patrol"]:
				return False
			return True

def radar_off(user, date_amount, time_amount, status, stats):
	start_check = False
	user_check = False
	#identifies the valid online user.
	radars = []
	for item in stats:
		if item["user"] == user:
			user_check = True
			if item["status"][1] == "online":
				start_check = True
				for radar in item["radars"]:
					#scans for the unclosed patrol
					#splices in the end timestamp.
					if radar["id"] == item["cur_radar"]:
						start = radar["start"]
						start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
						end = datetime.combine(date_amount, time_amount)
						radar["end"] = str(end)
						event_id = radar["id"]
						start = round_seconds(start)
						end = round_seconds(end)
					radar["user"] = item["user"]
					radars.append(radar)

				total_radars = get_total_patrols(radars, item["user"])
				#calculates the length of the patrol
				duration = end - start
				stats[stats.index(item)]["status"][1] = status
				stats[stats.index(item)]["cur_radar"] = None
				return stats, duration, len(item["radars"]), total_radars, event_id, None

	if not user_check:
		return stats, None, None, None, None, 3
	elif not start_check:
		return stats, None, None, None, None, 2

def confirm_radar(stats, user_id):
	for user in stats:
		if user_id == user["user"]:
			if user["cur_radar"]:
				return False
			return True