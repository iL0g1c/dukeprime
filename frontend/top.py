from datetime import datetime, date, timedelta
from operator import itemgetter

from patrols import get_total_patrols

def do_top(stats, mode, span):
	mode_check = False
	span_check = False
	#span is day, week, month
	#mode is patrols, patrol_time, kills, disables, sars

	if mode in ("patrols", "patrol_time", "kills", "disables", "sars", "radars", "radar_time"):
		mode_check = True
	if span in ("day", "week", "month", "all"):
		span_check = True

	if not mode_check:
		return stats, None, 10
	elif not span_check:
		return stats, None, 11
		
	#gets the constants for the different parameters.
	day_date = date.today()
	day = datetime(day_date.year, day_date.month, day_date.day)
	week_date = day_date - timedelta(days=((day_date.isoweekday() + 1) % 7)) + timedelta(days=1)
	week = datetime(week_date.year, week_date.month, week_date.day, 0, 0, 0)
	month = datetime(day_date.year, day_date.month, 1)

	candids = []
	if mode == "patrol_time":
		mode_type = "patrols"
	elif mode == "radar_time":
		mode_type = "radars"
	else:
		mode_type = mode
	#identifies all events in valid timespan.
	for user in stats:
		for item in user[mode_type]:
			item["user"] = user["user"]
			if item["end"] == None:
				continue
			mode_time = datetime.strptime(item["end"], "%Y-%m-%d %H:%M:%S.%f")
			if span == "day" and mode_time >= day:
				candids.append(item)
			elif span == "week" and mode_time >= week:
				candids.append(item)
			elif span == "month" and mode_time >= month:
				candids.append(item)
			elif span == "all":
				candids.append(item)
	users = list(map(itemgetter("user"), stats))
	counts = {}
	#uses the events to create a table holding
	#the number of patrols for each user.
	for candid in candids:
		for user in users:
			if not(mode == "patrol_time" or mode == "radar_time"):
				if not (user in counts):
					counts[user] = 0
				if candid["user"] == user:
					counts[user] += 1
			else:
				counts[user] = get_total_patrols(candids, user)
	#sorts the users by patrol count.
	n = len(counts)
	counts = list(counts.items())
	for i in range(n):
		for j in range(0, n-i-1):
			if counts[j][1] < counts[j+1][1]:
				counts[j], counts[j+1] = counts[j+1], counts[j]
	return stats, counts, None