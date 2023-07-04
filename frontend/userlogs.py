from datetime import datetime

from patrols import round_seconds

def do_userlogs(stats, pilot, type):
	logs = []
	user_check = False#initializes error catch checks
	type_check = False
	for user in stats:
		if user["user"] == pilot:#finds specified user
			user_check = True
			if type == "kills" or type == "disables" or type == "patrols" or type == "radars" or type == "sars":
				type_check = True
			else:
				break
			#cycles through all the the events of the
			#specified type.
			for item in user[type]:
				#depending on type of event it will extract and
				#calculate the valid data.
				if type == "kills" or type == "disables":
					type_check = True
					logs.append({
						"id": item["id"],
						"time": item["end"]
					})
					
				elif type == "patrols" or type == "radars":
					type_check = True
					start = item["start"]
					if item["end"]:#checks to see if the patrol is open.
						end = item["end"]
						#calculates the duration.
						start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
						end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")
						start = round_seconds(start)
						end = round_seconds(end)
						dur = end - start
					else:
						dur = "<open>"
						end = "<open>"
					logs.append({
						"id": item["id"],
						"start": item["start"],
						"end": str(end),
						"dur": dur
					})
					
				elif type == "sars":
					type_check = True
					logs.append({
						"id": item["id"],
						"time": item["end"]
					})
	if not user_check:
		return None, 7
	if not type_check:
		return None, 16
	return logs, None