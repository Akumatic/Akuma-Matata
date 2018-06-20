# Akuma Matata

A Discord Bot written in Python using the Rewrite API wrapper

## Getting Started

### Prerequisites
- Python 3.6
- Discord Rewrite API Wrapper

##### You can get the Wrapper with pip:
`python -m pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip`

Depending on your OS and environment you need to type `python3` or another equivalent instead of `python`

### Setting it up
1. Go [to your Discord's App Overview](https://discordapp.com/developers/applications/me) and create a new app.
2. Scroll down and "Create a Bot User"
3. Reveal and copy Token of your new Bot
4. Open [settings.json](settings.json) and paste your Token into the quotes after `"token":`

### Start the Bot
Just open a console and type ```python akuma.py```

Depending on your OS and environment you need to type `python3` or another equivalent instead of `python`

## Add your own extensions
It is easy to create a new extension on your own. First you need to create a new python file in the "extensions" folder.

You'll need this code in the newly created file: 
```
class Name():
    def __init__(self, bot):
        self.bot = bot

#Setup
def setup(bot):
    bot.add_cog(Name(bot))
```

Just replace "Name" in Line 1 and 6 by an own class name. A new command needs to be a member of this class.

Instead of using `@bot.command()` you'll need to use `@commands.command()`. 

The first argument of a method needs to be `self`.

##### An Example:
```
from discord.ext import commands

class PingPong():
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def ping(self, ctx):
    	await ctx.send("Pong")

#Setup
def setup(bot):
    bot.add_cog(PingPong(bot))
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details