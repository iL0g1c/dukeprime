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

def write_log(event_id, datetime_amount, server_id, user_id, action):
    with open(f"/var/www/backend/database-beta/log.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow((event_id, datetime_amount, server_id, user_id, action))
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
    else:
        users = database.users
        users.insert_one({
            "user_id": user_id,
            "server_id": server_id,
            "sar_needed": False,
            "superuser": False
        })
        return log_on(user_id, server_id, datetime_amount)
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
    else:
        return None, 1
    print("hello world")

def radar_on(user_id, server_id, datetime_amount):
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
        radars = list(database.radars.find({
        "$and": [
            {"$and": [
                {"user_id": Int64(user_id)},
                {"server_id": Int64(server_id)}
            ]},
            {"end": {"$type": 10}}
        ]
    }))
    else:
        users = database.users
        users.insert_one({
            "user_id": user_id,
            "server_id": server_id,
            "sar_needed": False,
            "superuser": False
        })
        return radar_on(user_id, server_id, datetime_amount)
    if radars == []:
        start_check = True
        event_id = get_id()
        radars = database.radars
        radars.insert_one({
            "event_id": event_id,
            "user_id": user_id,
            "server_id": server_id,
            "start": datetime_amount,
            "end": None
        })
        return event_id, None
    else:
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
        else:
            return None, None, None, None, 2
    else:
        return None, None, None, None, 3

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

def radar_off(user_id, server_id, datetime_amount):
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
        radar_filter = {
            "$and": [
                {"$and": [
                {"user_id": Int64(user_id)},
                {"server_id": Int64(server_id)}
                ]},
                {"end": {"$type": 10}}
            ]
        } 
        radars = list(database.radars.find(radar_filter))
        if radars != []:
            start_check = True
            start = radars[0]["start"]
            end = datetime_amount
            event_id = radars[0]["event_id"]
            
            radar_data = database.radars
            radar_data.update_one(radar_filter, {"$set": {"end": end}})
            
            total_radar_time = get_total_time(user_id, server_id)
            
            #calculates the length of the patrol
            duration = end - start
            return duration, len(radars), total_radar_time, event_id, None
        else:
            return None, None, None, None, 2
    else:
        return None, None, None, None, 3

def confirm_radar(user_id, server_id):
    radars = list(database.radars.find({
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
    if radars == []:
        return True
    return False
    
def do_kill(user_id, server_id, datetime_amount):
    user_check = False
    #identifies the valid online user.
    users = list(database.users.find({
        "$and": [
            {"user_id": Int64(user_id)},
            {"server_id": Int64(server_id)}
        ]
    }))
    if users != []:
        user_check = True
        #adds an entry log for the kill
        event_id = get_id()
        kill_data = database.kills
        kill_data.insert_one({
            "event_id": event_id,
            "user_id": user_id,
            "server_id": server_id,
            "time": datetime_amount
        })
        kills = len(list(database.kills.find({
            "$and": [
                {"user_id": Int64(user_id)},
                {"server_id": Int64(server_id)}
            ]
        })))
        disables = len(list(database.disables.find({
            "$and": [
                {"user_id": Int64(user_id)},
                {"server_id": Int64(server_id)}
            ]
        })))
        return kills, disables, event_id, None
    else:
        return None, None, None, 3
def do_disable(user_id, server_id, datetime_amount):
    user_check = False
    #identifies the valid online user.
    users = list(database.users.find({
        "$and": [
            {"user_id": Int64(user_id)},
            {"server_id": Int64(server_id)}
        ]
    }))
    if users != []:
        user_check = True
        #adds an entry log for the kill
        event_id = get_id()
        disable_data = database.disables
        disable_data.insert_one({
            "event_id": event_id,
            "user_id": user_id,
            "server_id": server_id,
            "time": datetime_amount
        })
        kills = len(list(database.kills.find({
            "$and": [
                {"user_id": Int64(user_id)},
                {"server_id": Int64(server_id)}
            ]
        })))
        disables = len(list(database.disables.find({
            "$and": [
                {"user_id": Int64(user_id)},
                {"server_id": Int64(server_id)}
            ]
        })))
        return kills, disables, event_id, None
    else:
        return None, None, None, 3

def record_sar(user_id, server_id, datetime_amount, action, pilot_id):
    action_check = False
    pilot_check = False
    no_pilot_check = False
    user_check = False
    sar_start_check = False
    sar_end_check = False
    user_filter = {
        "$and": [
            {"user_id": Int64(user_id)},
            {"server_id": Int64(server_id)}
        ]
    }
    users = list(database.users.find(user_filter))
    user_check = True
    if action == "req":
        sar_end_check = True
        action_check = True
        if pilot_id == None:
            no_pilot_check = True
        else:
            return None, None, 5
        #updates the sar_needed variable to log the request.
        if users[0]["sar_needed"] == "no":
            sar_start_check = True
            user_data = database.users
            user_data.update_one(
                user_filter,
                {"$set": {"sar_needed": "yes"}}
            )
        else:
            return None, None, 6
        count = None
        event_id = None
    elif action == "give":
        action_check = True
        sar_start_check = True
        no_pilot_check = True
        pilot_filter = {
            "$and": [
                {"user_id": Int64(pilot_id)},
                {"server_id": Int64(server_id)}
            ]
        }
        pilot = list(database.users.find(pilot_filter))
        if pilot != []:
            pilot_check = True
            if pilot[0]["sar_needed"] == "yes":
                sar_end_check = True
                user_data = database.users
                user_data.update_one(
                    pilot_filter,
                    {"$set": {"sar_needed": "no"}}
                )
            else:
                return None, None, 8
        else:
            return None, None, 7
        event_id = get_id()
        sar_data = database.sars
        sar_data.insert_one({
            "event_id": event_id,
            "user_id": user_id,
            "server_id": server_id,
            "pilot_id": pilot_id,
            "time": datetime_amount
        })
        count = len(list(database.sars.find({
            "$and": [
                {"user_id": Int64(user_id)},
                {"server_id": Int64(server_id)}
            ]
        })))
    else:
        return None, None, 3
    return count, event_id, None

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

def do_top(server_id, mode, span):
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
    if span == "day":
        period = datetime(day_date.year, day_date.month, day_date.day)
    elif span == "week":
        week_date = day_date - timedelta(days=((day_date.isoweekday() + 1) % 7)) + timedelta(days=1)
        period = datetime(week_date.year, week_date.month, week_date.day, 0, 0, 0)
    elif span == "month":
        period = datetime(day_date.year, day_date.month, 1)

    if mode == "patrols":
        patrol_filter = {
            "$and": [
                {"end": {"$gte": period}},
                {"server_id": Int64(server_id)}
            ]
        }
        patrols = list(database.patrols.find(patrol_filter))
        print(patrols)
    elif mode == "patrol_time":
        pass
    elif mode == "kills":
        pass
    elif mode == "disables":
        pass
    elif mode == "sars":
        pass
    elif mode == "radars":
        pass
    elif mode == "radar_time":
        pass

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
    datetime_amount = datetime.now().replace(microsecond=0)
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
    datetime_amount = datetime.now().replace(microsecond=0)
    time_zone = datetime_amount.astimezone().tzinfo
    
    embed = discord.Embed(title="Radar Event",
                            description=f"{ctx.message.author.mention} has started their patrol.",
                            color=0xFF5733)
    embed.add_field(name="Name: ", value=ctx.message.author.mention)
    embed.add_field(name="Date: ", value=str(datetime_amount.date()))
    embed.add_field(name="Time: ", value=str(f"{time_zone}: {datetime_amount.time().strftime('%H:%M:%S')}"))
    embed.add_field(name="Action: ", value="Online")
    
    event_id, error = radar_on(ctx.message.author.id, ctx.message.guild.id, datetime_amount)
    
    if error:
        action = f"Radar Patrol Start Error Code: {error}"
        await ctx.send(get_error(error))
    else:
        action = "Radar Patrol Start"
        embed.add_field(name="Event ID: ", value=event_id)
        await ctx.send(embed=embed)

    write_log(event_id, str(datetime_amount), str(ctx.message.guild.id), str(ctx.message.author.id), action)

@bot.command(brief="Log when you get offline.", description="Log when you get offline.")
async def off(ctx):
    user_id = ctx.message.author.id
    server_id = ctx.message.guild.id
    
    datetime_amount = datetime.now().replace(microsecond=0)
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

    write_log(event_id, str(datetime_amount), str(server_id), str(user_id), action)
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
    user_id = ctx.message.author.id
    server_id = ctx.message.guild.id
    
    datetime_amount = datetime.now().replace(microsecond=0)
    time_zone = datetime_amount.astimezone().tzinfo
    
    embed = discord.Embed(title="Radar Event",
                         description=f"{ctx.message.author.mention} has ended their patrol.",
                         color=0xFF5733)
    embed.add_field(name="Name: ", value=ctx.message.author.mention)
    embed.add_field(name="Date: ", value=str(datetime_amount.date()))
    embed.add_field(name="Time: ", value=str(f"{time_zone}: {datetime_amount.time()}"))
    embed.add_field(name="Action: ", value="Offline")
    duration, patrols, total, event_id, error = radar_off(user_id, server_id, datetime_amount)
    
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

    write_log(event_id, str(datetime_amount), str(server_id), str(user_id), action)
    logged = confirm_radar(user_id, server_id)
    if not logged:
        await ctx.send("An error has occured and your patrol has not been logged. Try closing your patrol again.")
        me = bot.get_user(786382147531440140)
        await me.send("Ghostbug detected.")
        await me.send("Isolating patrol data...")
        message = f"Name: {ctx.message.author.name} \nDate: {datetime_amount.date()} \nTime: {datetime_amount.time()}\nTotal Patrols: {patrols}\nTotal Time: {total}\nEvent ID: {event_id}\nDuration: {duration}"
        await me.send(message)

@bot.command(brief="Log when you get a kill.", description="Log when you get a kill.")
async def kill(ctx):
    user_id = ctx.message.author.id
    server_id = ctx.message.guild.id
    
    datetime_amount = datetime.now().replace(microsecond=0)
    time_zone = datetime_amount.astimezone().tzinfo
    
    embed = discord.Embed(title="Flight Event",
                         description=f"{ctx.message.author.mention} has killed a foe.",
                         color=0xFF5733)
    embed.add_field(name="Name: ", value=ctx.message.author.mention)
    embed.add_field(name="Date: ", value=str(datetime_amount.date()))
    embed.add_field(name="Time: ", value=str(f"{time_zone}: {datetime_amount.time()}"))
    embed.add_field(name="Action: ", value="Kill")
    kills, disables, event_id, error = do_kill(user_id, server_id, datetime_amount)

    write_log(event_id, str(datetime_amount), str(server_id), str(user_id), "Kill")
    
    if error:
        await ctx.send(get_error(error))
    else:
        embed.add_field(name="Event ID: ", value=event_id)
        embed.set_footer(text=f"{ctx.message.author} has {kills} kills and {disables} Disables.")
        await ctx.send(embed=embed)

@bot.command(brief="Log when you disable someone.", description="Log when you disable someone.")
async def disable(ctx):
    user_id = ctx.message.author.id
    server_id = ctx.message.guild.id
    
    datetime_amount = datetime.now().replace(microsecond=0)
    time_zone = datetime_amount.astimezone().tzinfo
    
    embed = discord.Embed(title="Flight Event",
                         description=f"{ctx.message.author.mention} has disabled a foe.",
                         color=0xFF5733)
    embed.add_field(name="Name: ", value=ctx.message.author.mention)
    embed.add_field(name="Date: ", value=str(datetime_amount.date()))
    embed.add_field(name="Time: ", value=str(f"{time_zone}: {datetime_amount.time()}"))
    embed.add_field(name="Action: ", value="Disable")
    kills, disables, event_id, error = do_disable(user_id, server_id, datetime_amount)

    write_log(event_id, str(datetime_amount), str(server_id), str(user_id), "Disable")
    
    if error:
        await ctx.send(get_error(error))
    else:
        embed.add_field(name="Event ID: ", value=event_id)
        embed.set_footer(text=f"{ctx.message.author} has {kills} kills and {disables} Disables.")
        await ctx.send(embed=embed)

@bot.command(brief="Log when you confirm a foe.", description="Log when you confirm a foe.")
async def foe(ctx):
    datetime_amount = datetime.now().replace(microsecond=0)
    time_zone = datetime_amount.astimezone().tzinfo
    embed = discord.Embed(title="Flight Event",
                         description=f"{ctx.message.author.mention} has spotted a foe.",
                         color=0xFF5733)
    embed.add_field(name="Name: ", value=ctx.message.author.mention)
    embed.add_field(name="Date: ", value=str(datetime_amount.date()))
    embed.add_field(name="Time: ", value=str(f"{time_zone}: {datetime_amount.time()}"))
    embed.add_field(name="Action: ", value="Foe")
    await ctx.send(embed=embed)

@bot.command(brief="Log when you give and need SAR.", description="Log when you give and need SAR. Action is either <req> (request an SAR) or <give> (give an SAR). When you give an SAR specify the <pilot>.")
async def sar(ctx, action, pilot: discord.User = None):
    user_id = ctx.message.author.id
    server_id = ctx.message.guild.id
    
    datetime_amount = datetime.now().replace(microsecond=0)
    time_zone = datetime_amount.astimezone().tzinfo
    embed = discord.Embed(title="Flight Event",
                         description=f"{ctx.message.author.mention} is requesting SAR.",
                         color=0xFF5733)
    embed.add_field(name="Name: ", value=ctx.message.author.mention)
    embed.add_field(name="Date: ", value=str(datetime_amount.date()))
    embed.add_field(name="Time: ", value=str(f"{time_zone}: {datetime_amount.time()}"))
    if action == "req":
        log_action = "SAR Request"
        embed.add_field(name="Action: ", value="SAR Request")
    elif action == "give":
        log_action = "SAR Given"
        embed.add_field(name="Action: ", value="SAR Given")
    if pilot != None:
        pilot = pilot.id
    count, event_id, error = record_sar(user_id, server_id, datetime_amount, action, pilot)
    if error:
        await ctx.send(get_error(error))
        log_action = f"{log_action}| Error code: {error}"
    else:
        if action == "give":
            embed.add_field(name="SARs: ", value=str(count))
            embed.add_field(name="Event ID: ", value=event_id)
        await ctx.send(embed=embed)
    write_log(event_id, str(datetime_amount), str(server_id), str(user_id), log_action)
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
async def top(ctx, mode, span="month"):
    server_id = ctx.message.guild.id

    datetime_amount = datetime.now().replace(microsecond=0)
    time_zone = datetime_amount.astimezone().tzinfo

    results, ranks, error = do_top(server_id, mode, span)
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
