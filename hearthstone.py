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
# Get an API key from https://market.mashape.com/omgvamp/hearthstone

hearth_rx = re.compile('\[(.+?)\]')

# Bot gibberish
thank_yous = ['thank you', 'god bless', 'bless you', 'much  obliged', 'thanks', 'thx', 'gracias', 'merci', 'danke', 'much obliged']
try_agains = ['try more letters', 'type smarter words', 'how about a better set of words', 'try again', 'don\'t you look silly']

# Comedy cards
# Not actual cards but I want the bot to respond as if it was, jokes you see.
comedy_cards = {
                'blood manos' : {'title': 'Blood Manos', 'url': 'http://i.imgur.com/a5fXYW4.png', 'source': 'http://imgur.com/a/IEUSR', 'color': 'Legendary'},
                'kink banana' : {'title': 'Kink Banana', 'url': 'http://i.imgur.com/AML3T27.png', 'source': 'http://imgur.com/a/IEUSR', 'color': 'Common'},
                }

def trigger(message):
    query = re.search(hearth_rx, message.content.lower().strip())
    if query and query.groups()[0].strip():
        return True

async def action(message, client):
    # Get the search query from inside the []
    query = re.search(hearth_rx, message.content.lower().strip())
    query = query.groups()[0].strip()

    if query in comedy_cards.keys():
        embed_message = Embed(title = comedy_cards[query]['title'],
                              type = 'rich',
                              url = comedy_cards[query]['source'])
        embed_message.set_image(url = comedy_cards[query]['url'])
        embed_message.color = _set_color(comedy_cards[query]['color'])
        await client.send_message(message.channel, embed = embed_message)

    # Run the search
    results = hearthstone_card_search(query)

    if results:
        cards_to_remove = []
        for card in results:
            if card['type'] not in ('Minion', 'Spell', 'Weapon') \
                    or card['cardSet'] in ('Debug', 'Tavern Brawl')  \
                    or card['name'] in ('Jade Golem'):
                    or 'flavor' not in card.keys():
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
            embed_message.color = _set_color(card['rarity'])
            await client.send_message(message.channel, embed = embed_message)

        elif len(results) > 1 and len(results) < 10:
            for result_card in results:
                if query == result_card['name'].lower():
                    embed_message = Embed(title = result_card['name'],
                                          type = 'rich',
                                          url = 'http://www.hearthpwn.com/search?search={0}#t1:cards'.format(urllib.parse.quote_plus(result_card['name'])))
                    embed_message.set_footer(text = result_card['flavor'])
                    embed_message.set_image(url = _random_gold(result_card))
                    embed_message.color = _set_color(result_card['rarity'])
                    await client.send_message(message.channel, embed = embed_message)
                    return
            msg = 'Multiple results found: *{0}*'.format(", ".join([x['name'] for x in results]))
            await client.send_message(message.channel, msg)
        elif len(results) >= 10:
            msg = '{0} results found, {2}, {1}.'.format(len(results), random.choice(thank_yous), random.choice(try_agains))
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
    if card == 'Free':
        return Color.light_grey()
    elif card == 'Common':
        return Color.lighter_grey()
    elif card == 'Rare':
        return Color.blue()
    elif card == 'Epic':
        return Color.purple()
    elif card == 'Legendary':
        return Color.orange()
    else:
        return Color.default()
