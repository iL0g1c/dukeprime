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