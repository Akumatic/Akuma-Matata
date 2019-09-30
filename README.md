# Akuma Matata

A Discord Bot written in Python using the Rewrite API Wrapper

## Getting Started

### Prerequisites
- Python 3.6
- Discord Rewrite API Wrapper

##### You can get the Wrapper with pip:
`python -m pip install discord.py`

Depending on your OS and environment you need to type `python3` or another equivalent instead of `python`

### Initial setup
1. Go to [your Discord's App Overview](https://discordapp.com/developers/applications/me) and create a new app.
2. Scroll down and "Create a Bot User"
3. Reveal and copy Token of your new Bot
4. Start the Bot (see below)
5. The Bot will ask you for the Token. Paste it.
7. Go to [your Discord's App Overview](https://discordapp.com/developers/applications/me) again and open the Bot
8. Click on "Generate OAuth2 URL" and give the bot `Administrator` Bot Permissions
9. Open the generated URL and add the Bot to your Server

### Start the Bot
Just open a console and type ```python akuma.py```

Depending on your OS and environment you need to type `python3` or another equivalent instead of `python`

### Configuration


The configuration files for the bot are now stored in %APPDATA%, $XDG_CONFIG_HOME or ~/.config. The specific directory for these files is `Akumatic/Akuma-Matata`. However is a direct interaction with them not necessary anymore.


## Add your own extensions
It is easy to create a new extension on your own. First you need to create a new python file in the "extensions" folder.

You'll need this code in the newly created file: 
```
from discord.ext import commands

class Name(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#Setup
def setup(bot):
    bot.add_cog(Name(bot))
```

Just replace "Name" in Line 1 and 6 by an own class name. A new command needs to be a member of this class.

Instead of using `@bot.command()` you'll need to use `@commands.command()`. 

The first argument of a method needs to be `self`.

After implementing all your functions, you just need to load the extension with the following command in any channel your bot can listen to: `load <extension>`

If you add `true`to your command, the extension will be added to your configuration files and gets automatically loaded on start.

##### An Example:
```
from discord.ext import commands

class PingPong(commands.Cog):
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