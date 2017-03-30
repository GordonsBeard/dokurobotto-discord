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

    if message.content == "!fut" or message.content == "!simp":
        simpsons_screen = True
        if message.content == "!fut":
            simpsons_screen = False

        random_screen = frinkiac.random(simpsons_screen)
        random_screen._get_details()
        embed_message = Embed(type = 'rich', url = random_screen.rich_url, title = 'S{0}E{1} {2}'.format(random_screen.season, random_screen.ep_number, random_screen.ep_title))
        embed_message.set_image(url = random_screen.meme_url())
        embed_message.set_footer(text = '{0}'.format(random_screen.wiki_link))
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
                search[0]._get_details()
                if query.startswith('"') and query.endswith('"'):
                    embed_message = Embed(type = 'rich', url = search[0].rich_url, title = 'S{0}E{1} {2}'.format(search[0].season, search[0].ep_number, search[0].ep_title))
                    embed_message.set_image(url = search[0].meme_url(caption = query.split('"')[1]))
                    await client.send_message(message.channel, embed = embed_message)
                else:
                    embed_message = Embed(type = 'rich', url = search[0].rich_url, title = 'S{0}E{1} {2}'.format(search[0].season, search[0].ep_number, search[0].ep_title))
                    embed_message.set_image(url = search[0].meme_url())
                    embed_message.set_footer(text = '{0}'.format(search[0].wiki_link))
                    await client.send_message(message.channel, embed = embed_message)
        except ValueError:
            await client.add_reaction(message, '?')