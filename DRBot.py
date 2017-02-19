import discord
from discord.ext import commands

import snooplinks, hearthstone, frink
plugins_list = [ snooplinks, frink, hearthstone ]

from config import client_key
client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot == True:
        return

    # # Message dispatcher
    for plugin in plugins_list:
        if plugin.trigger(message) == True:
            await plugin.action(message, client)
            return

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(client_key)