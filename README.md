- pycord is neccesary to easily use slash_commands, which enables autocomplete and descriptions for commands
    - When using commands, remember to invite bot using the application.commands (and bot) scope 
- remember to enable message_content_intent:
    - https://discord.com/developers/applications/1142437189523869727/bot

Some resources used during the creation:

pycord docs
https://guide.pycord.dev/interactions/application-commands/slash-commands

pycord help, because docs were not precise
https://stackoverflow.com/questions/71165431/how-do-i-make-a-working-slash-command-in-discord-py

Context (ctx) attributes 
https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Context

bot invite link
https://discord.com/api/oauth2/authorize?client_id=1142437189523869727&permissions=2048&scope=bot%20applications.commands

httpx docs
https://www.python-httpx.org/advanced/

create discord embed
https://stackoverflow.com/questions/44862112/how-can-i-send-an-embed-via-my-discord-bot-w-python
https://discordpy.readthedocs.io/en/stable/api.html#embed


static coc data
https://coc.guide/static/json/heroes.json
- index:
boosters.json
buildings.json
capital_buildings.json
capital_characters.json
capital_obstacles.json
capital_projectiles.json
capital_spells.json
capital_traps.json
characters.json
client_globals.json
globals.json
heroes.json
languages.json
object_ids.json
obstacles.json
pass_tasks.json
pets.json
projectiles.json
replay.json
spells.json
supers.json
tasks.json
townhall_levels.json
traps.json
upgrade_tasks.json
weapons.json

plot dataframe table
https://stackoverflow.com/questions/32137396/how-do-i-plot-only-a-table-in-matplotlib

adjust table
https://towardsdatascience.com/simple-little-tables-with-matplotlib-9780ef5d0bc4

adjust plot canvas size to table
https://stackoverflow.com/questions/42987799/saving-matplotlib-table-creates-a-lot-of-whitespace

api proxy to get around whitelisting dynamic ip adresses
https://docs.royaleapi.com/proxy.html

# Modules
if using py-cord, discord.py needs to be uninstalled