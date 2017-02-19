from discord import Embed
from discord import Color
import requests
import random
import re
import urllib
from config import mashape_key

# Hearthstone Card Identification
# Condition: [search term]
# Action: Returns info about the card, or < 10 search results.

hearth_rx = re.compile('\[(.+?)\]')

def trigger(message):
    query = re.search(hearth_rx, message.content.lower().strip())
    if query and query.groups()[0].strip():
        return True

async def action(message, client):
    query = re.search(hearth_rx, message.content.lower().strip())
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
            embed_message = Embed(title = card['name'], 
                                  type = 'rich', 
                                  url = 'http://www.hearthpwn.com/search?search={0}#t1:cards'.format(urllib.parse.quote_plus(card['name'])))
            embed_message.set_footer(text = card['flavor'])
            embed_message.set_image(url = _random_gold(card))
            embed_message.color = _set_color(card)
            await client.send_message(message.channel, embed = embed_message)

        elif len(results) > 1 and len(results) < 10:
            for result_card in results:
                if query.groups()[0].strip().lower() == result_card['name'].lower():
                    embed_message = Embed(title = result_card['name'],
                                          type = 'rich',
                                          url = 'http://www.hearthpwn.com/search?search={0}#t1:cards'.format(urllib.parse.quote_plus(result_card['name'])))
                    embed_message.set_footer(text = result_card['flavor'])
                    embed_message.set_image(url = _random_gold(result_card))
                    embed_message.color = _set_color(result_card)
                    await client.send_message(message.channel, embed = embed_message)
                    return
            msg = 'Multiple results found: *{0}*'.format(", ".join([x['name'] for x in results]))
            await client.send_message(message.channel, msg)
        elif len(results) >= 10:
            msg = '{0} results found, {2}, {1}.'.format(len(results), random.choice(['thank you', 'god bless', 'bless you', 'much  obliged', 'thanks', 'thx', 'gracias', 'merci', 'danke', 'much obliged']), random.choice(['try more letters', 'type smarter words', 'how about a better set of words', 'try again', 'don\'t you look silly']))
            await client.send_message(message.channel, msg)

def hearthstone_card_search(q):
    url = "https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/{0}"
    headers={"X-Mashape-Key": mashape_key}
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

def _set_color(card):
    if card['rarity'] == 'Free':
        return Color.light_grey()
    elif card['rarity'] == 'Common':
        return Color.lighter_grey()
    elif card['rarity'] == 'Rare':
        return Color.blue()
    elif card['rarity'] == 'Epic':
        return Color.purple()
    elif card['rarity'] == 'Legendary':
        return Color.orange()
    else:
        return Color.default()