import discord
from discord.ext import commands
import random
import re
import requests
import frinkiac

from config import key as client_key
from discord import Emoji

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message.content = message.content.lower()

    # Snooplinks
    # Only works in #meatspace / #bots
    # 1/5 chance of posting a video whenever 'weed' is mentioned.
    # 4/4 chance of emoji-replying with :weed: otherwise.
    rx = re.compile('(wee+d)')
    if re.search(rx, message.content.lower()):
        line = random.choice(list(open('snooplinks.txt')))
        if message.channel.id in ['263827420774137857', '249803171642212364']:
            if random.choice([1,2,3,4,5]) == 1: # 4/20 choice to post a video
                msg = '<{0}>'.format(line)
                await client.send_message(message.channel, msg)
            else:
                weedmoj = Emoji(server = 'Cafe of Broken Dreams', id = '260293426401116160')
                await client.add_reaction(message, weedmoj)
    
    # Hearthstone card search
    # Looks for [card name]
    rx = re.compile('\[(.+?)\]')
    query = re.search(rx, message.content.lower().strip())
    if query and query.groups()[0].strip():
        if query.groups()[0].strip().lower() == 'death wish':
            msg = '**Why Do You Keep Searching This**\nhttps://hydra-media.cursecdn.com/hearthstone.gamepedia.com/9/9c/Death_Wish.png'
            await client.send_message(message.channel, msg)
        results = hearthstone_card_search(query.groups()[0].strip())
        cards_to_remove = []

        if results:
            for card in results:
                if card['type'] not in ('Minion', 'Spell', 'Weapon') or card['cardSet'] in ('Debug', 'Tavern Brawl') or card['name'] in ('Jade Golem') or 'flavor' not in card.keys():
                    cards_to_remove.append(card)

            for card in cards_to_remove:
                results.remove(card)

            if len(results) == 1:
                card = results[0]
                msg = '**{0}**\n{1}'.format(card['name'], _random_gold(card))
                await client.send_message(message.channel, msg)
            elif len(results) > 1 and len(results) < 10:
                for result_card in results:
                    if query.groups()[0].strip().lower() == result_card['name'].lower():
                        msg = '**{0}**\n{1}'.format(result_card['name'], _random_gold(result_card))
                        await client.send_message(message.channel, msg)
                        return
                msg = 'Multiple results found: *{0}*'.format(", ".join([x['name'] for x in results]))
                await client.send_message(message.channel, msg)
            elif len(results) >= 10:
                msg = '{0} results found, {2}, {1}.'.format(len(results), random.choice(['thank you', 'god bless', 'bless you', 'much  obliged', 'thanks', 'thx', 'gracias', 'merci', 'danke', 'much obliged', 'duh..', ]), random.choice(['try more letters', 'type smarter words', 'how about a better set of words', 'try again', 'give up', 'don\'t you look silly']))
                await client.send_message(message.channel, msg)
    
    # Frinkiac / Simpsons Search
    # Looks for:
    # !simp
    # !simp search string
    if message.content.startswith("!simp") or message.content.startswith("!fut"):
        if message.content == "!simp":
            random_screen = frinkiac.random()
            await client.send_message(message.channel, random_screen.meme_url())
        elif message.content == "!fut":
            random_screen = frinkiac.random(False)
            await client.send_message(message.channel, random_screen.meme_url())
        else:
            try:
                if message.content.startswith("!simp"):
                    command, query = message.content.split("!simp ")
                    search = frinkiac.search(query)
                elif message.content.startswith("!fut"):
                    command, query = message.content.split("!fut ")
                    search = frinkiac.search(query, False)
                if search:
                    if query.startswith('"') and query.endswith('"'):
                        await client.send_message(message.channel, search[0].meme_url(caption = query.split('"')[1]))
                    else:
                        await client.send_message(message.channel, search[0].meme_url())
                else:
                    await client.add_reaction(message, '❔')
            except ValueError:
                await client.add_reaction(message, '❔')

def hearthstone_card_search(q):
    url = "https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/{0}"
    headers={"X-Mashape-Key": "xNq3M7EO99msht1Kh2Bv26QRkDcSp1gD0Q8jsniTmOabV665Bf"}
    response = requests.get(url.format(q), headers=headers)
    dictionary = response.json()
    if 'message' in dictionary:
        dictionary = {}
    return dictionary

def _random_gold(card):
    if random.choice(range(1,100)) == 1:
        image = card['imgGold']
    else:
        image = card['img']
    return image

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(client_key)