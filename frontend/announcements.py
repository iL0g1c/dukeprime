def do_setannounce(guilds, server, channel):
	guild_check = False
	for guild in guilds:
		if guild["id"] == server:
			guild_check = True
			guilds[guilds.index(guild)]["announce"] = channel

	if not guild_check:
		return guilds, 15
	return guilds, None