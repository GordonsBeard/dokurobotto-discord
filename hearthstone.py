import requests
import random
import re
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