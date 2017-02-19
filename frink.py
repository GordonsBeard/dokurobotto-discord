from discord import Embed
import frinkiac

# Frinkiac / Simpsons Search
# Looks for:
# !simp
# !simp search string

def trigger(message):
    if message.content.startswith("!simp") or message.content.startswith("!fut"):
        return True

async def action(message, client):
    message.content = message.content.lower()
    if message.content == "!simp":
        random_screen = frinkiac.random()
        embed_message = Embed(type = 'rich')
        embed_message.set_image(url = random_screen.meme_url())
        await client.send_message(message.channel, embed = embed_message)
    elif message.content == "!fut":
        random_screen = frinkiac.random(False)
        embed_message = Embed(type = 'rich')
        embed_message.set_image(url = random_screen.meme_url())
        await client.send_message(message.channel, embed = embed_message)
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
                    embed_message = Embed(type = 'rich')
                    embed_message.set_image(url = search[0].meme_url(caption = query.split('"')[1]))
                    await client.send_message(message.channel, embed = embed_message)
                else:
                    embed_message = Embed(type = 'rich')
                    embed_message.set_image(url = search[0].meme_url())
                    await client.send_message(message.channel, embed = embed_message)
        except ValueError:
            await client.add_reaction(message, '?')