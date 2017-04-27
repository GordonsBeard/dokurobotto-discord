import random

# Rolls a dice in NdN format.

def trigger(message):
    if message.content.lower().startswith('!roll'):
        return True

async def action(message, client):
    if message.content.lower().strip() == '!roll':
        rolls = 1
        limit = 6
    else:
        dice = message.content.split('!roll ')[1]
        rolls, limit = map(int, dice.split('d'))
        if int(limit) > 53594 or rolls > 100:
            return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await client.send_message(message.channel, result)
