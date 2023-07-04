from files import get_id
from datetime import datetime

def record_sar(user, date_amount, time_amount, action, pilot, stats):
	action_check = False
	pilot_check = False
	no_pilot_check = False
	user_check = False
	sar_start_check = False
	sar_end_check = False
	if action == "req":
		action_check = True
		#locates the user.
		for item in stats:
			if item["user"] == user:
				user_check = True
				if pilot == None:
					no_pilot_check = True
				#updates the sar_needed variable to log the request.
				if stats[stats.index(item)]["sar_needed"] == "no":
					sar_start_check = True
					stats[stats.index(item)]["sar_needed"] = "yes"
					return stats, None, None, None
	elif action == "give":
		sar_start_check = True
		action_check = True
		no_pilot_check = True
		for item in stats:
			if item["user"] == pilot:
				pilot_check = True
				if item["sar_needed"] == "yes":
					sar_end_check = True
					#reverts the sar request back to normal.
					item["sar_needed"] = "no"
		for item in stats:
			if item["user"] == user:
				user_check = True
				#adds a an sar event log to the user
				#that did the SAR
				id = get_id()
				item["sars"].append({
					"id": id,
					"end": str(datetime.combine(date_amount, time_amount)),
					"pilot": pilot
				})
				count = len(item["sars"])
	if not user_check:
		if not action_check:
			return stats, None, None, 4
		return stats, None, None, 3
	elif not no_pilot_check:
		return stats, None, None, 5
	elif not sar_start_check:
		return stats, None, None, 6
	elif not pilot_check:
		return stats, None, None, 7
	elif not sar_end_check:
		return stats, None, None, 8
	else:
		return stats, count, id, None