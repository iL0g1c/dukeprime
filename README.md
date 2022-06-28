# Duke Prime</br>User Manual

## Introduction
DukePrime is a groundbreaking discord bot built to streamline mrp record keeping tasks including logging patrols, sars, kills, and disables. DukePrime stores all of these statistics into a datafile for each server, so that bot crashes do not lead to data loss. Additionally, these statistics are ready to be retrieved by the air force at any time.

## Basic Commands
In the follow commands <> and [] denote parameters. Replace the <text> with your input.
<> means the parameter is required. [] means the parameter is optional. In optional parameters, "=" specifies the default parameter.

### ```register```
### Use:
This is a legacy command that used to be required in order to register your server with our registry.
It is now done automatically when your bot is added, but if for some reason it doesn't use this command.
**You cannot use other commands until you register your server.**

### ```on```
### Use:
Use this to start your patrol.
Even if your server is registered a specific user can not use the bot unless they have used ```on``` or ```radon``` at least once.

### ```off```
### Use:
Use this to end your patrol. It will return timestamps along with your patrol duration and total patrols and hours.

### ```radon```
### Use:
This is the same as the “on” command except to log a radar patrol. This will also create your user record in your servers files.

### ```radoff```
### Use:
This is the same as the “off” command except to log a radar patrol.

### ```kill```
### Use:
This command logs a kill. It will log your timestamp as well as both your kill and disable totals.

### ```disable```
### Use:
This command logs a disable. It will log your timestamp as well as both your kill and disable totals.

### ```foe```
### Use:
This command reports a foe sighting to your server. This is not stored in your server files as it is just an alert with the timestamp of the spotting.

### ```ping```
### Use:
To test your latency to the bot.

### ```sar <action: give|req> [pilot: @mention]```
### Use:
The action is either “give” or “req.” Request will alert your server that you need sar. Give will log that you SARed someone.
If you are giving an SAR you must specify the "pilot" parameter

### ```top <type: patrols|patrol_time|radars|radar_time|sars|kills|disables> [span = month: day|week|month|all]```
### Use:
The type is which statistic you would like to view.
The span is the timespan that you would like to view your patrols in.

### ```test```
###Use:
To start a quiz in which you can practice your missile countermeasures.

### ```userlogs <pilot: @mention> <type: patrols|radars|kills|disables|sars>```
### Use:
To view all of a certain <type> of event for a certain <pilot>
For <pilot> you must mention a user.
For <type> you can choose an event type.

## Admin Commands
These commands can only be used by someone how is registered in the bot as an admin **NOT** the admin role on the server.
### ```cradmin <user: @mention>```
### Use:
Is used to add bot admin abilities to a user.
Without running this command you can not use admin commands.
**You must have the manage roles permission to use this command.
The user must be registered in your server in order to receive this ability.**

### ```remev <event_id>```
### Use:
Use this command to remove any event from your servers files.
Any event that has the event id on the log can be removed.
You can find the ID on the log for the event that you want to delete.
**In order to use this command you must have been added as a bot admin using the “cradmin” command.**

