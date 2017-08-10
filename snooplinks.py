from discord import Emoji
import random
import re

from config import channel_list as chans

# Snooplinks
# Only works in #meatspace / #bots
# 1/5 chance of posting a video whenever 'weed' is mentioned.
# 4/5 chance of emoji-replying with :weed: otherwise.

def trigger(message):
    message.content = message.content.lower()
    rx = re.compile('(wee+d)')
    if re.search(rx, message.content.lower()) and message.channel.id in [chans['#meatspace'], chans['#bots'], chans['#cafe-420']]:
        return True

async def action(message, client):
    line = random.choice(list(open('snooplinks.txt')))
    if random.choice([1,2,3,4,5]) == 1: # 4/20 choice to post a video
        msg = '<{0}>'.format(line)
        await client.send_message(message.channel, msg)
    else:
        weedmoj = Emoji(server = 'Cafe of Broken Dreams', id = '260293426401116160')
        await client.add_reaction(message, weedmoj)
