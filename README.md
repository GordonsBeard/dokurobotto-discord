# dokurobotto-discord
Dokurobotto on Discord, now with fewer features!

Come see it in action at the Cafe: [https://discord.gg/NKnPGb3](https://discord.gg/NKnPGb3)

Setup
---
1) Make sure you're running Python 3.5+

2) Install the things listed in [requirements.txt](requirements.txt)

2a) You'll need a copy of [frinkiac.py](https://github.com/GordonsBeard/frinkiac.py)

3) Generate `config.py` with the following information:

```
client_key = '<your discord bot client key>'
mashape_key = '<your mashape hearthstone key>'
channel_list = {'#yourchan' : '<chanid>',}
```

4) Modify `DRBot.py` to remove any plugins from the plugins_list you do not wish to use. (For instance, snooplinks will only work in specific channels on a specific server unless modified.)

```
import snooplinks, hearthstone, frink
plugins_list = [ snooplinks, frink, hearthstone]
```

5) `python DRBot.py`

Current Features
---
**Frinkiac / Morbotron**

Type `!simp` or `!fut` followed by a search, and you'll get the related Simpsons/Futurama screenshot in response.

If you add quotation marks around your search, it will label the search with those quotes, a fun pseudo-randomizer.
![Frinkiac module at work](http://i.imgur.com/T59XGTR.png)

**Hearthstone Card Info**

Type `[card name]` and get the picture of the Hearthstone card, and its flavor text.
![Hearthstone card information](http://i.imgur.com/eonISVO.png)

**Snooplinks**

(a dumb joke for a dumb channel please do not judge)
Type the word `weed` anywhere, and DR will respond with a :weed: emoji 16/20 times and a snooplink video the remainder of the time.
![Snooplinks at work](http://i.imgur.com/lFtLc78.png)
