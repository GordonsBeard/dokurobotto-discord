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
        except ValueError:
            await client.add_reaction(message, '?')