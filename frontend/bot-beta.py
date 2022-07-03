import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, date, timedelta, timezone
from dateutil.relativedelta import relativedelta
import jsonlines
import json
from operator import itemgetter
import random
import csv
from dotenv import load_dotenv, find_dotenv
import pprint
from pymongo import MongoClient
from bson import Int64

load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = "mongodb://mongo_db_admin:password@45.76.164.130:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.5.0"
client = MongoClient(connection_string)
database = client.dukeprime

def load_prefix(bot, message):
  guild = list(database.guilds.find({"server_id": message.guild.id}))[0]
  if guild == None:
    return "=prime "
  return guild["prefix"]

def get_total_time(user_id, server_id):
	patrols = list(database.patrols.find({
	  "$and": [
	    {"user_id": user_id},
	    {"server_id": server_id}
	  ]
	}))
	
	total = timedelta(seconds=0)
	for i in range(len(patrols)):
		#scans through all of the patrols,
		#and extracts all of the times and,
		#then totals them all up.
		start = patrols[i]["start"]
		end = patrols[i]["end"]
		duration = end - start
		total += duration
	return total

def get_id():
	#everytime a new event is created,
	#it is assigned the next id in the
	data = list(database.global_data.find())[0]
	database.global_data.update_one({"ids": data["ids"]}, {"$inc": {"ids": 1}})
	data["ids"] += 1
	return data["ids"]

def get_error(code):
	#Takes in an error code and returns the error
	#message to be printed to the screen.
	if code == 1:
		return "You have already started your patrol."
	elif code == 2:
		return "You have not started a patrol yet."
	elif code == 3:
		return "Could not find you in your servers registry.\n Register yourself by starting a patrol with <on>"
	elif code == 4:
		return "Invalid action parameter. Please use either req or give."
	elif code == 5:
		return "The request action does not take a pilot parameter."
	elif code == 6:
		return "You have already requested an SAR."
	elif code == 7:
		return "Could not find that pilot in your server's registry."
	elif code == 8:
		return "This pilot has not requested an SAR."
	elif code == 9:
		return "You have already registered your server in the registry."
	elif code == 10:
		return "Invalid parameter for mode. Use 'patrols', 'patrol_time', 'kills', 'disables', or 'sars'"
	elif code == 11:
		return "Invalid parameter for span. Use 'day', 'week', or 'month'."
	elif code == 12:
		return "Could not find that user in your server's registry."
	elif code == 13:
		return "You must have the Manage Roles permission to user this command."
	elif code == 14:
		return "Could not find that event identifier in your servers registry."
	elif code == 15:
		return "You have not registered your server yet. Register it with the 'register' command."
	elif code == 16:
		return "Invalid parameter for type. Use 'patrols', 'radars', 'kills', 'disables', or 'sars'"
	elif code == 17:
		return "You are not a DukePrime admin. Have a person with 'manage roles' use the cradmin command to add you."

def get_missiles():
	return [
		["Matra R.511",1],
		["Matra R.530",1],
		["Matra Super 530F/Super 530D",1],
		["Sedjil",1],
		["Al Humurrabi",1],
		["Aspide",1],
		["R-40RD",1],
		["R-23R",1],
		["R-24R",1],
		["R-33",1],
		["R-27R/R-27R1",1],
		["R-27ER/R-27ER1",1],
		["R-77P/RVV-PE",1],
		["R-37",1],
		["AIM-7",1],
		["Sparrow",1],
		["AIM-9C Sidewinder",1],
		["Izdeliye 140",1],
		["Izdeliye 340",1],
		["MAA-1A Piranha",2],
		["MAA-1B Piranha",2],
		["A-Darter",2],
		["Matra R.510",2],
		["Matra R.550 Magic",2],
		["R530E",2],
		["Matra Magic II",2],
		["MICA-IR",2],
		["IRIS-T Fatter",2],
		["Python (Shafrir 1/2 | Python 3/4/5)",2],
		["AAM-3",2],
		["AAM-5",2],
		["PL-5B/C/E",2],
		["PL-8",2],
		["PL-9 (PL-9C)",2],
		["PL-10/PL-ASR",2],
		["K-13",2],
		["R-40TD",2],
		["R-23T",2],
		["R-24T",2],
		["R-60",2],
		["R-27T/R-27T1",2],
		["R-27ET/R-27ET1",2],
		["R-73",2],
		["R-73M",2],
		["R-74M/RVV-MD/R-74M2",2],
		["R-77T/RVV-TE",2],
		["V3 Kukri",2],
		["Sky Sword I (TC-1)",2],
		["AIM-9 Sidewinder",2],
		["AIM-92 Stinger",2],
		["AIM-132 ASRAAM",2],
		["Bozdoğan (Merlin)",2],
		["K-MD",2],
		["RVV-MD",2],
		["Izdeliye 160",2],
		["Izdeliye 300",2],
		["Izdeliye 310",2],
		["Izdeliye 320",2],
		["Izdeliye 360",2],
		["Izdeliye 740",2],
		["Izdeliye 750",2],
		["Izdeliye 760",2],
		["MICA-EM",3],
		["Astra Mk.I",3],
		["K-100",3],
		["Fakour-90",3],
		["Derby (Alto)",3],
		["AAM-4",3],
		["PL-12 (SD-10)",3],
		["F80",3],
		["PL-15",3],
		["R-33S",3],
		["R-27EA",3],
		["R-27EM",3],
		["R-77/RVV-AE",3],
		["R-77-1/RVV-SD",3],
		["KS-172",3],
		["R-Darter",3],
		["AIM-120 AMRAAM",3],
		["Sky Sword II (TC-2)",3],
		["Izdeliye 170",3],
		["Izdeliye 172",3],
		["Izdeliye 180",3],
		["Izdeliye 190",3],
		["Izdeliye 610",3],
		["Izdeliye 810",3]
	]

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

def write_log(event_id, time_stamp, guild_id, user_id, action):
	with open(f"/var/www/backend/database-beta/log.csv", "a") as f:
		writer = csv.writer(f)
		writer.writerow((event_id, time_stamp, guild_id, user_id, action))
	f.close()

def log_on(user_id, server_id, datetime_amount):
  user_check = False
  start_check = False
  users = list(database.users.find({
    "$and": [
      {"user_id": Int64(user_id)},
      {"server_id": Int64(server_id)}
    ]
  }))
  if users != []:
    user_check = True
    patrols = list(database.patrols.find({
      "$and": [
          {"$and": [
            {"user_id": Int64(user_id)},
            {"server_id": Int64(server_id)}
          ]},
          {"end": {"$type": 10}}
        ]
    }))
    if patrols == []:
      start_check = True
      event_id = get_id()
      patrols = database.patrols
      patrols.insert_one({
        "event_id": event_id,
        "user_id": user_id,
        "server_id": server_id,
        "start": datetime_amount,
        "end": None
      })
      return event_id, None
  if not user_check:
    users = database.users
    users.insert_one({
      "user_id": user_id,
      "server_id": server_id,
      "sar_needed": False,
      "superuser": False
    })
    return log_on(user_id, server_id, datetime_amount)
  elif not start_check:
    return None, 1

def radar_on(user_id, server_id, date_amount, time_amount):
	user_check = False
	start_check = False
	users = list(database.users.find({
    "$and": [
      {"user_id": Int64(user_id)},
      {"server_id": Int64(server_id)}
    ]
  }))
  if users != []:
    user_check = True
    start = datetime.combine(date_amount, time_amount)
    radars = list(database.radars.find({
      "$and": [
          {"$and": [
            {"user_id": Int64(user_id)},
            {"server_id": Int64(server_id)}
          ]},
          {"end": {"$type": 10}}
        ]
    }))
    if radars == []:
      start_check = True
      event_id = get_id()
      radars = database.radars
      radars.insert_one({
        "event_id": event_id,
        "user_id": user_id,
        "server_id": server_id,
        "start": str(start),
        "end": None
      })
      return event_id, None
  if not user_check:
    users = database.users
    users.insert_one({
      "user_id": user_id,
      "server_id": server_id,
      "sar_needed": False,
      "superuser": False
    })
    return radar_on(user_id, server_id, date_amount, time_amount)
  elif not start_check:
    return None, 1

def log_off(user_id, server_id, datetime_amount):
  user_check = False
  start_check = False
  #identifies the valid online user.
  users = list(database.users.find({
    "$and": [
      {"user_id": Int64(user_id)},
      {"server_id": Int64(server_id)}
    ]
  }))
  if users != []:
    user_check = True
    patrol_filter = {
      "$and": [
          {"$and": [
            {"user_id": Int64(user_id)},
            {"server_id": Int64(server_id)}
          ]},
          {"end": {"$type": 10}}
        ]
    }
    patrols = list(database.patrols.find(patrol_filter))
    if patrols != []:
      start_check = True
      start = patrols[0]["start"]
      end = datetime_amount
			event_id = patrols[0]["event_id"]
			
			patrol_data = database.patrols
			patrol_data.update_one(patrol_filter, {"$set": {"end": end}})
			
			total_patrol_time = get_total_time(user_id, server_id)
			
			#calculates the length of the patrol
			duration = end - start
			return duration, len(patrols), total_patrol_time, event_id, None

	if not user_check:
		return None, None, None, None, 3
	elif not start_check:
		return None, None, None, None, 2

def confirm_patrol(user_id, server_id):
  patrols = list(database.patrols.find({
    "$and": [
      {
        "$and": [
          {"user_id": user_id},
          {"server_id": server_id}
        ]
      },
      {"end": {"$type": 10}}
    ]
  }))
	if patrols == []:
		return True
	return False

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

def do_register(server_id, guilds):
    guild_check = True
    #scans to make sure the guild has not already
    #been registered.
    for item in guilds:
      if item["server_id"] == server_id:
        guild_check = False
    
    if not guild_check:
    	return guilds, 9
    		
    #if not it adds the entry in the guild
    #collection
    database.guilds.insert_one({
      "server_id": server_id,
      "announcement_channel": None,
      "prefix": "=prime "
    })
    
    return guilds, None

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

def do_setannounce(guilds, server, channel):
	guild_check = False
	for guild in guilds:
		if guild["id"] == server:
			guild_check = True
			guilds[guilds.index(guild)]["announce"] = channel

	if not guild_check:
		return guilds, 15
	return guilds, None

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
		

intents = discord.Intents.default()
intents.members = True
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#An internal function that will make sure the data structure carries over.
#registry_trans()
bot = commands.Bot(intents=intents, command_prefix=load_prefix, help_command=None)
#all the commands below,
#1. load the stats for the guild.
#2. start creating an embed for the response.
#3. run the function that processes the data. (above)
#4. sends an error message if an error was returned.
#5. sends the embed.
#6. stores the updated stats back the in guilds
#personal database.
@bot.event
async def on_ready():
	print(f"{bot.user} has connected to Discord!")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Geo-FS"))
	activeservers = bot.guilds
	full_guilds = []
	for guild in activeservers:
		print(guild.name)
		full_guilds.append(guild)
	#await load_channels(full_guilds)

@bot.command(brief="Test the connection.", description="Test the connection.")
async def ping(ctx):
	delay = round(bot.latency * 1000)
	await ctx.send(f"PONG!\n {delay}ms")

@bot.event
async def on_guild_join(guild):
	guilds = list(database.guilds.find())
	guilds, error = do_register(guild.id, guilds)
	if error:
		await guild.text_channels[0].send("Make sure to register yourself with the 'register' command")
	else:
		await guild.text_channels[0].send("Your server has been automatically registered.\n If you would like recieve updates on known bugs, and new features run the 'setannounce' command in the announcements channel.\n DISCLAIMER: Duke will not use this feature for advertising purposes.")

@bot.command(brief="Log when you get online.", description="Log when you get online.")
async def on(ctx):
  datetime_amount = datetime.now(timezone.utc).replace(microsecond=0)
	time_zone = datetime_amount.astimezone().tzinfo
	
	embed = discord.Embed(title="Patrol Event",
						  description=f"{ctx.message.author.mention} has started their patrol.",
						  color=0xFF5733)
	embed.add_field(name="Name: ", value=ctx.message.author.mention)
	embed.add_field(name="Date: ", value=str(datetime_amount.date()))
	embed.add_field(name="Time: ", value=str(f"{time_zone}: {datetime_amount.time().strftime('%H:%M:%S')}"))
	embed.add_field(name="Action: ", value="Online")
	
	event_id, error = log_on(ctx.message.author.id, ctx.message.guild.id, datetime_amount)
	
	if error:
		action = f"Patrol Start Error Code: {error}"
		await ctx.send(get_error(error))
	else:
		action = "Patrol Start"
		embed.add_field(name="Event ID: ", value=event_id)
		await ctx.send(embed=embed)

	write_log(event_id, str(datetime_amount), str(ctx.message.guild.id), str(ctx.message.author.id), action)

@bot.command(brief="Log when you get on radar.", description="Log when you get on radar.")
async def radon(ctx):
	date_amount = date.today()
	time_amount = datetime.now().time()
	time_zone = datetime.now(timezone.utc).astimezone().tzinfo
	embed = discord.Embed(title="Radar Event",
						  description=f"{ctx.message.author.mention} has started their patrol.",
						  color=0xFF5733)
	embed.add_field(name="Name: ", value=ctx.message.author.mention)
	embed.add_field(name="Date: ", value=str(date_amount))
	embed.add_field(name="Time: ", value=str(f"{time_zone}: {time_amount.strftime('%H:%M:%S')}"))
	embed.add_field(name="Action: ", value="Online")
	event_id, error = radar_on(ctx.message.author.id, ctx.message.guild.id, date_amount, time_amount)
	
	if error:
		action = f"Radar Patrol Start Error Code: {error}"
		await ctx.send(get_error(error))
	else:
		action = "Radar Patrol Start"
		embed.add_field(name="Event ID: ", value=event_id)
		await ctx.send(embed=embed)

	time_stamp = datetime.combine(date_amount, time_amount)
	write_log(event_id, time_stamp, str(ctx.message.guild.id), str(ctx.message.author.id), action)

@bot.command(brief="Log when you get offline.", description="Log when you get offline.")
async def off(ctx):
	user_id = ctx.message.author.id
	server_id = ctx.message.guild.id
	
	datetime_amount = datetime.now(timezone.utc).replace(microsecond=0)
	time_zone = datetime_amount.astimezone().tzinfo
	
	embed = discord.Embed(title="Patrol Event",
						 description=f"{ctx.message.author.mention} has ended their patrol.",
						 color=0xFF5733)
	embed.add_field(name="Name: ", value=ctx.message.author.mention)
	embed.add_field(name="Date: ", value=str(datetime_amount.date()))
	embed.add_field(name="Time: ", value=str(f"{time_zone}: {datetime_amount.time().strftime('%H:%M:%S')}"))
	embed.add_field(name="Action: ", value="Offline")
	
	duration, patrols, total, event_id, error = log_off(user_id, server_id, datetime_amount)
	
	if error:
		action = f"Patrol End Error Code: {error}"
		await ctx.send(get_error(error))
	else:
		action = "Patrol End"
		embed.add_field(name="Total Patrols: ", value=str(patrols))
		embed.add_field(name="Total Time: ", value=str(total))
		embed.add_field(name="Event ID: ", value=event_id)
		embed.set_footer(text=f"This patrol lasted {str(duration)}")
		await ctx.send(embed=embed)

	write_log(event_id, datetime_amount, str(server_id), str(user_id), action)
	logged = confirm_patrol(user_id, server_id)
	if not logged:
		await ctx.send("An error has occured and your patrol has not been logged. Try closing your patrol again.")
		me = bot.get_user(786382147531440140)
		await me.send("Ghostbug detected.")
		await me.send("Isolating patrol data...")
		message = f"Name: {ctx.message.author.name} \nDate: {datetime_amount.date()} \nTime: {datetime_amount.time()}\nTotal Patrols: {patrols}\nTotal Time: {total}\nEvent ID: {event_id}\nDuration: {duration}"
		await me.send(message)

@bot.command(brief="Log when you get offline.", description="Log when you get offline.")
async def radoff(ctx):
	stats, error=load_stats(ctx.message.guild.id)
	if error:
		await ctx.send(get_error(error))
		return
	user = ctx.message.author.id
	date_amount = date.today()
	time_amount = datetime.now().time()
	time_zone = datetime.now(timezone.utc).astimezone().tzinfo
	status = "offline"
	embed = discord.Embed(title="Radar Event",
						 description=f"{ctx.message.author.mention} has ended their patrol.",
						 color=0xFF5733)
	embed.add_field(name="Name: ", value=ctx.message.author.mention)
	embed.add_field(name="Date: ", value=str(date_amount))
	embed.add_field(name="Time: ", value=str(f"{time_zone}: {time_amount.strftime('%H:%M:%S')}"))
	embed.add_field(name="Action: ", value="Offline")
	stats, duration, patrols, total, event_id, error = radar_off(user, date_amount, time_amount, status, stats)
	
	if error:
		action = f"Radar Patrol End Error Code: {error}"
		await ctx.send(get_error(error))
	else:
		action = "Radar Patrol End"
		embed.add_field(name="Total Radar Patrols: ", value=str(patrols))
		embed.add_field(name="Total Time: ", value=str(total))
		embed.add_field(name="Event ID: ", value=event_id)
		embed.set_footer(text=f"This radar patrol lasted {str(duration)}")
		await ctx.send(embed=embed)
		save_stats(stats, ctx.message.guild.id)

	stats, error = load_stats(ctx.message.guild.id)
	logged = confirm_radar(stats, ctx.message.author.id)
	if not logged:
		await ctx.send("An error has occured and your patrol has not been logged. Try closing your patrol again.")
		me = bot.get_user(786382147531440140)
		await me.send("Ghostbug detected.")
		await me.send("Isolating patrol data...")
		message = f"Name: {ctx.message.author.name} \nDate: {date_amount} \nTime: {time_amount}\nTotal Patrols: {patrols}\nTotal Time: {total}\nEvent ID: {event_id}\nDuration: {str(duration)}"
		await me.send(message)

@bot.command(brief="Log when you get a kill.", description="Log when you get a kill.")
async def kill(ctx):
	stats, error=load_stats(ctx.message.guild.id)
	if error:
		await ctx.send(get_error(error))
		return
	user = ctx.message.author.id
	date_amount = date.today()
	time_amount = datetime.now().time()
	time_zone = datetime.now(timezone.utc).astimezone().tzinfo
	embed = discord.Embed(title="Flight Event",
						 description=f"{ctx.message.author.mention} has killed a foe.",
						 color=0xFF5733)
	embed.add_field(name="Name: ", value=ctx.message.author.mention)
	embed.add_field(name="Date: ", value=date_amount)
	embed.add_field(name="Time: ", value=str(f"{time_zone}: {time_amount.strftime('%H:%M:%S')}"))
	embed.add_field(name="Action: ", value="Kill")
	stats, kills, disables, event_id, error = do_kill(user, date_amount, time_amount, stats)

	time_stamp = datetime.combine(date_amount, time_amount)
	write_log(event_id, time_stamp, str(ctx.message.guild.id), str(user), "Kill")
	
	if error:
		await ctx.send(get_error(error))
	else:
		embed.add_field(name="Event ID: ", value=event_id)
		embed.set_footer(text=f"{ctx.message.author} has {kills} kills and {disables} Disables.")
		await ctx.send(embed=embed)
		save_stats(stats, ctx.message.guild.id)

@bot.command(brief="Log when you disable someone.", description="Log when you disable someone.")
async def disable(ctx):
	stats, error=load_stats(ctx.message.guild.id)
	if error:
		await ctx.send(get_error(error))
		return
	user = ctx.message.author.id
	date_amount = date.today()
	time_amount = datetime.now().time()
	time_zone = datetime.now(timezone.utc).astimezone().tzinfo
	embed = discord.Embed(title="Flight Event",
						 description=f"{ctx.message.author.mention} has disabled a foe.",
						 color=0xFF5733)
	embed.add_field(name="Name: ", value=ctx.message.author.mention)
	embed.add_field(name="Date: ", value=date_amount)
	embed.add_field(name="Time: ", value=str(f"{time_zone}: {time_amount.strftime('%H:%M:%S')}"))
	embed.add_field(name="Action: ", value="Disable")
	stats, kills, disables, event_id, error = do_disable(user, date_amount, time_amount, stats)
	
	time_stamp = datetime.combine(date_amount, time_amount)
	write_log(event_id, time_stamp, str(ctx.message.guild.id), str(user), "Disable")
	
	if error:
		await ctx.send(get_error(error))
	else:
		embed.add_field(name="Event ID: ", value=event_id)
		embed.set_footer(text=f"{ctx.message.author} has {kills} kills and {disables} Disables.")
		await ctx.send(embed=embed)
		save_stats(stats, ctx.message.guild.id)

@bot.command(brief="Log when you confirm a foe.", description="Log when you confirm a foe.")
async def foe(ctx):
	time_amount = datetime.now().time()
	time_zone = datetime.now(timezone.utc).astimezone().tzinfo
	embed = discord.Embed(title="Flight Event",
						 description=f"{ctx.message.author.mention} has spotted a foe.",
						 color=0xFF5733)
	embed.add_field(name="Name: ", value=ctx.message.author.mention)
	embed.add_field(name="Date: ", value=str(date.today()))
	embed.add_field(name="Time: ", value=str(f"{time_zone}: {time_amount.strftime('%H:%M:%S')}"))
	embed.add_field(name="Action: ", value="Foe")
	await ctx.send(embed=embed)

@bot.command(brief="Log when you give and need SAR.", description="Log when you give and need SAR. Action is either <req> (request an SAR) or <give> (give an SAR). When you give an SAR specify the <pilot>.")
async def sar(ctx, action, pilot: discord.User = None):
	stats, error=load_stats(ctx.message.guild.id)
	if error:
		await ctx.send(get_error(error))
		return
	user = ctx.message.author.id
	date_amount = date.today()
	time_amount = datetime.now().time()
	time_zone = datetime.now(timezone.utc).astimezone().tzinfo
	embed = discord.Embed(title="Flight Event",
						 description=f"{ctx.message.author.mention} is requesting SAR.",
						 color=0xFF5733)
	embed.add_field(name="Name: ", value=ctx.message.author.mention)
	embed.add_field(name="Date: ", value=str(date_amount))
	embed.add_field(name="Time: ", value=str(f"{time_zone}: {time_amount.strftime('%H:%M:%S')}"))
	if action == "req":
		log_action = "SAR Request"
		embed.add_field(name="Action: ", value="SAR Request")
	elif action == "give":
		log_action = "SAR Given"
		embed.add_field(name="Action: ", value="SAR Given")
	if pilot != None:
		pilot = pilot.id
	stats, count, event_id, error = record_sar(user, date_amount, time_amount, action, pilot, stats)

	time_stamp = datetime.combine(date_amount, time_amount)
	write_log(event_id, time_stamp, str(ctx.message.guild.id), str(user), log_action)
	
	if error:
		await ctx.send(get_error(error))
	else:
		if action == "give":
			embed.add_field(name="SARs: ", value=str(count))
			embed.add_field(name="Event ID: ", value=event_id)
		await ctx.send(embed=embed)
		save_stats(stats, ctx.message.guild.id)
@sar.error
async def info_error(ctx, error): # This might need to be (error, ctx), I'm not sure
    if isinstance(error, commands.BadArgument):
        await ctx.send(get_error(7))

@bot.command(brief="Register your server when you add this bot.", description="Register your server when you add this bot.")
async def register(ctx):
	guilds = load_guilds()
	id = ctx.message.guild.id
	guilds, error = do_register(id, guilds)
	time_stamp = datetime.now()
	write_log(None, time_stamp, str(ctx.message.guild.id), str(ctx.message.author.id), "Guild Registered")
	if error:
		await ctx.send(get_error(error))
	else:
		await ctx.send("Your server has been added to the registry.")
		save_guilds(guilds)

@bot.command(brief="View your militaries statistics.", description="The first parameter is the type of stats. This is either <patrols> <kill> <disables> or <sars>. The second parameter, optional, is the time span the patrols were taken in. Currently you can use <day> <week> or <month>. This defaults to week.")
async def top(ctx, type, span="month"):
	stats, error=load_stats(ctx.message.guild.id)
	if error:
		await ctx.send(get_error(error))
		return
	results, ranks, error = do_top(stats, type, span)
	if error:
		await ctx.send(get_error(error))
	else:
		leaderboard = ""
		for i in range(len(ranks)):
			member = ctx.guild.get_member(ranks[i][0])
			if member == None:
				#a check in case a user has logged
				#a patrol and then deleted their
				#account.
				#DP0007
				continue
			leaderboard += f"{i+1}. {member.display_name} | {type}: {ranks[i][1]}\n"
		embed = discord.Embed(title=f"{type} top", description=leaderboard, color=0xFF5733)
		await ctx.send(embed=embed)
		time_stamp = datetime.now()
		write_log(None, time_stamp, str(ctx.message.guild.id), str(ctx.message.author.id), "displayed top")

#used to create admins which can use admin commands
@bot.command(brief="Allows targeted user to use admmin commmands.", description="Allows targeted user to use admmin commmands. You must have the Manage Roles permission to use this command.")
async def cradmin(ctx, user: discord.User):
	if not ctx.message.author.guild_permissions.administrator:
		error = 13
	stats, error=load_stats(ctx.message.guild.id)
	if error:
		await ctx.send(get_error(error))
		return
	stats, error = do_cradmin(stats, user.id)
	if error:
		await ctx.send(get_error(error))
	else:
		await ctx.send(f"Made {user.mention} a DukePrime admin.")
		save_stats(stats, ctx.message.guild.id)
		time_stamp = datetime.now()
		write_log(None, time_stamp, str(ctx.message.guild.id), str(ctx.message.author.id), "Created an admin.")
	
#error detection for an invalid user entry.
@cradmin.error
async def user_error(ctx, error): # This might need to be (error, ctx), I'm not sure
    if isinstance(error, commands.BadArgument):
        await ctx.send(get_error(12))

#Allows an admin to remove an event from the
#registry.
@bot.command(brief="Remove an event from a targeted user.", description="Remove an event from a targeted user. You must be a registered bot admin. (given through 'cradmin')")
async def remev(ctx, event_id):
	stats, error=load_stats(ctx.message.guild.id)
	if error:
		await ctx.send(get_error(error))
		return
	stats, error = do_remev(stats, event_id, ctx.message.author.id)
	if error:
		await ctx.send(get_error(error))
	else:
		await ctx.send(f"Removed event '{event_id}' from your servers registry.")
		save_stats(stats, ctx.message.guild.id)
		time_stamp = datetime.now()
		write_log(None, time_stamp, str(ctx.message.guild.id), str(ctx.message.author.id), "Removed an event.")

@bot.command(brief="Sets a channel where you will here updates for DukePrime.", description="Sets a channel where you will here updates for DukePrime.")
async def setannounce(ctx):
	guilds = load_guilds()
	server = ctx.message.guild.id
	channel = ctx.message.channel.id
	stats, error = do_setannounce(guilds, server, channel)
	if error:
		await ctx.send(get_error(guilds, error))
	else:
		await ctx.send("DukePrime announcements will be sent in this channel.")
		save_guilds(guilds)
		time_stamp = datetime.now()
		write_log(None, time_stamp, str(ctx.message.guild.id), str(ctx.message.author.id), "Set an announcement channel.")

@bot.command(brief="Developer Command.", description="Developer Command.")
async def announcement(ctx):
	if ctx.message.author.id in [786382147531440140]:
		guilds = load_guilds()
		messages = await bot.get_channel(ctx.message.channel.id).history(limit=2).flatten()
		result = []
		for msg in messages:
			result.append(msg.content)
		for guild in guilds:
			if "announce" in guild:
				channel = bot.get_channel(guild["announce"])
				await channel.send(result[1])
		time_stamp = datetime.now()
		write_log(None, time_stamp, str(ctx.message.guild.id), str(ctx.message.author.id), "Broadcasted an announcement.")
	else:
		await ctx.send("You are not a developer.")

@tasks.loop(seconds=1.0)
async def do_test(ctx):
	#checks for answer
	def check(m):
		return m.content
		
	#generates random missile.
	missiles = get_missiles()
	num = random.randint(0, len(missiles))
	question_one = await ctx.send(missiles[num][0])
	await bot.get_channel(ctx.message.channel.id).history(limit=2).flatten()

	#fetches responses and checks if answer is valid.
	response_one = await bot.wait_for("message", check=check)
	try:
		if int(response_one.content) == missiles[num][1]:
			answer = await ctx.send("Correct.")
		else:
			answer = await ctx.send(f"Incorrect:\nFox {missiles[num][1]}")
	except:
		answer = await ctx.send("Invalid input.")
	#asks if user wants to continue.
	question_two = await ctx.send("Continue? (y/n)")
	await bot.get_channel(ctx.message.channel.id).history(limit=2).flatten()
	response_two = await bot.wait_for("message", check=check)
	
	#delets all if the comments.
	await question_one.delete()
	await response_one.delete()
	await answer.delete()
	await question_two.delete()
	await response_two.delete()
	if response_two.content == "n":
		await do_test.cancel()

@bot.command(brief="a test on missile countermeasures.", description="a test on missile countermeasures.")
async def test(ctx):
	await do_test.start(ctx)

@bot.command(brief="View all of a certain users log type.", description="View all of a certain users log type. pilot is a mentioned user. type is 'patrols', 'radars', 'kills', 'disables', or 'sars'.")
async def userlogs(ctx, pilot: discord.User, type):
	stats, error = load_stats(ctx.message.guild.id)
	if error:
		await ctx.send(get_error(error))
		return
	logs, error = do_userlogs(stats, pilot.id, type)
	if error:
		await ctx.send(get_error(error))
		return
	log_text = ""
	for item in logs: #cycles through all of the events and
					  #formats them for the embed.
		if type == "kills" or type == "disables":
			log_text += f"**id:** {item['id']}, **time:** {item['time']}\n"
		elif type == "patrols" or type == "radars":
			log_text += f"**id:** {item['id']}, **start time:** {item['start']}, **end time:** {item['end']}, **duration:** {item['dur']}\n"
		elif type == "sars":
			log_text += f"**id:** {item['id']}, **time:** {item['time']}\n"
	
	log_text = f"**Total {type}: {len(logs)}**\n" + log_text
	embed = discord.Embed(title=f"{pilot.display_name}'s {type} log.", description=log_text, color=0xFF5733)
	await ctx.send(embed=embed)
@userlogs.error
async def pilot_error(ctx, error): # This might need to be (error, ctx), I'm not sure
    if isinstance(error, commands.BadArgument):
        await ctx.send(get_error(7))

@bot.command(brief="help")#custom help command
#links users to the duke discord server and the docs.
async def help(ctx):
	embed = discord.Embed(title="Help", description="Hello! You can read the docs at: https://github.com/iL0g1c/dukeprime#readme\n Or if you have farther questions you can contact Duke at: https://discord.gg/qYmdfA4NGa", color=0xFF5733)
	await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def prefix(ctx, token):
	stats, error = load_stats(ctx.message.guild.id)
	if error:
		await ctx.send(get_error(error))
		return
	error = do_prefix(stats, token, ctx.message.author.id, ctx.message.guild.id)
	if error:
		await ctx.send(get_error(error))
		return
	await ctx.message.guild.me.edit(nick=f"[{token}] DukePrime|Beta")
	await ctx.send("Changed my prefix to: " + token)
	time_stamp = datetime.now()
	write_log(None, time_stamp, str(ctx.message.guild.id), str(ctx.message.author.id), "Changed prefix.")

#runs the bot
#TOKEN = os.environ['bot_token']
bot.run(TOKEN)
