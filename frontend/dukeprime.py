import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, date, timezone
import os
import random

from admin import load_prefix
from files import load_guilds, save_guilds, do_register, load_stats, save_stats
from errors import get_error
from patrols import log_on, log_off, radar_on, radar_off, confirm_patrol, confirm_radar
from logs import write_log
from wins import do_disable, do_kill
from sars import record_sar
from top import do_top
from admin import do_cradmin, do_prefix, do_remev
from announcements import do_setannounce
from missiles import get_missiles
from userlogs import do_userlogs

intents = discord.Intents.all()
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

@bot.command(brief="Test the connection.", description="Test the connection.")
async def ping(ctx):
	delay = round(bot.latency * 1000)
	await ctx.send(f"PONG!\n {delay}ms")

@bot.event
async def on_guild_join(guild):
	guilds = load_guilds()
	guilds, error = do_register(guild.id, guilds)
	if error == 9:
		await guild.text_channels[0].send("Thanks for adding back DukePrime! Your old server records have been restored.")
	elif error:
		await guild.text_channels[0].send(f"Error in registering your server.\n ERROR: {get_error(error)}\n Try using =register to register manually.\n If this does not work you can seek technical assistance from Duke Knight Systems: https://discord.gg/qYmdfA4NGa")
	else:
		await guild.text_channels[0].send("Your server has been automatically registered.\n If you would like recieve updates on known bugs, and new features run the 'setannounce' command in the announcements channel.\n DISCLAIMER: Duke will not use this feature for advertising purposes.")
		save_guilds(guilds)

@bot.command(brief="Log when you get online.", description="Log when you get online.")
async def on(ctx):
	stats, error=load_stats(ctx.message.guild.id)
	if error:
		await ctx.send(get_error(error))
		return
	user = ctx.message.author.id
	date_amount = date.today()
	time_amount = datetime.now().time()
	time_zone = datetime.now(timezone.utc).astimezone().tzinfo
	status = "online"
	embed = discord.Embed(title="Patrol Event",
						  description=f"{ctx.message.author.mention} has started their patrol.",
						  color=0xFF5733)
	embed.add_field(name="Name: ", value=ctx.message.author.mention)
	embed.add_field(name="Date: ", value=str(date_amount))
	embed.add_field(name="Time: ", value=str(f"{time_zone}: {time_amount.strftime('%H:%M:%S')}"))
	embed.add_field(name="Action: ", value="Online")
	stats, event_id, error = log_on(user, date_amount, time_amount, status, stats)
	if error:
		action = f"Patrol Start Error Code: {error}"
		await ctx.send(get_error(error))
	else:
		action = "Patrol Start"
		embed.add_field(name="Event ID: ", value=event_id)
		await ctx.send(embed=embed)
		save_stats(stats, ctx.message.guild.id)

	time_stamp = datetime.combine(date_amount, time_amount)
	write_log(event_id, time_stamp, str(ctx.message.guild.id), str(user), action)

@bot.command(brief="Log when you get on radar.", description="Log when you get on radar.")
async def radon(ctx):
	stats, error=load_stats(ctx.message.guild.id)
	if error:
		await ctx.send(get_error(error))
		return
	user = ctx.message.author.id
	date_amount = date.today()
	time_amount = datetime.now().time()
	time_zone = datetime.now(timezone.utc).astimezone().tzinfo
	status = "online"
	embed = discord.Embed(title="Radar Event",
						  description=f"{ctx.message.author.mention} has started their patrol.",
						  color=0xFF5733)
	embed.add_field(name="Name: ", value=ctx.message.author.mention)
	embed.add_field(name="Date: ", value=str(date_amount))
	embed.add_field(name="Time: ", value=str(f"{time_zone}: {time_amount.strftime('%H:%M:%S')}"))
	embed.add_field(name="Action: ", value="Online")
	stats, event_id, error = radar_on(user, date_amount, time_amount, status, stats)
	
	if error:
		action = f"Radar Patrol Start Error Code: {error}"
		await ctx.send(get_error(error))
	else:
		action = "Radar Patrol Start"
		embed.add_field(name="Event ID: ", value=event_id)
		await ctx.send(embed=embed)
		save_stats(stats, ctx.message.guild.id)

	time_stamp = datetime.combine(date_amount, time_amount)
	write_log(event_id, time_stamp, str(ctx.message.guild.id), str(user), action)

@bot.command(brief="Log when you get offline.", description="Log when you get offline.")
async def off(ctx):
	stats, error=load_stats(ctx.message.guild.id)
	if error:
		await ctx.send(get_error(error))
		return
	user = ctx.message.author.id
	date_amount = date.today()
	time_amount = datetime.now().time()
	time_zone = datetime.now(timezone.utc).astimezone().tzinfo
	status = "offline"
	embed = discord.Embed(title="Patrol Event",
						 description=f"{ctx.message.author.mention} has ended their patrol.",
						 color=0xFF5733)
	embed.add_field(name="Name: ", value=ctx.message.author.mention)
	embed.add_field(name="Date: ", value=str(date_amount))
	embed.add_field(name="Time: ", value=str(f"{time_zone}: {time_amount.strftime('%H:%M:%S')}"))
	embed.add_field(name="Action: ", value="Offline")
	stats, duration, patrols, total, event_id, error = log_off(user, date_amount, time_amount, status, stats)
	
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
		save_stats(stats, ctx.message.guild.id)

	time_stamp = datetime.combine(date_amount, time_amount)
	write_log(event_id, time_stamp, str(ctx.message.guild.id), str(user), action)
	
	stats, error = load_stats(ctx.message.guild.id)
	logged = confirm_patrol(stats, ctx.message.author.id)
	if not logged:
		await ctx.send("An error has occured and your patrol has not been logged. Try closing your patrol again.")
		me = bot.get_user(786382147531440140)
		await me.send("Ghostbug detected.")
		await me.send("Isolating patrol data...")
		message = f"Name: {ctx.message.author.name} \nDate: {date_amount} \nTime: {time_amount}\nTotal Patrols: {patrols}\nTotal Time: {total}\nEvent ID: {event_id}\nDuration: {str(duration)}"
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
	
	history = []
	async for message in bot.get_channel(ctx.message.channel.id).history(limit=2):
		history.append(message)
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
	history = []
	async for message in bot.get_channel(ctx.message.channel.id).history(limit=2):
		history.append(message)
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
	await ctx.message.guild.me.edit(nick=f"[{token}]DukePrime")
	await ctx.send("Changed my prefix to: " + token)
	time_stamp = datetime.now()
	write_log(None, time_stamp, str(ctx.message.guild.id), str(ctx.message.author.id), "Changed prefix.")

#runs the bot
#TOKEN = os.environ['bot_token']
bot.run(TOKEN)
