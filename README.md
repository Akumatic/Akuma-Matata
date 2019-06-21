# Akuma Matata

A Discord Bot written in Python using the Rewrite API wrapper

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
4. Open [settings.json](settings.json) and paste your Token into the quotes after `"token":`
5. Open Discord, enable Developer Mode (Settings > Appearance) and copy your own ID
6. Open [settings.json](settings.json) and paste your ID into the quotes after `"maintainer":`
6. Start the Bot (see below)
7. Go to [your Discord's App Overview](https://discordapp.com/developers/applications/me) again and open the Bot
8. Click on "Generate OAuth2 URL" and give the bot `Administrator` Bot Permissions
9. Open the generated URL and add the Bot to your Server

### Start the Bot
Just open a console and type ```python akuma.py```

Depending on your OS and environment you need to type `python3` or another equivalent instead of `python`

### Configuration

In your bot folder are two configuration files: `settings.json` and `server.json`.

##### settings.json

- `token`

The bot token your bot is using. 

- `prefix`

The bot needs a prefix to distinguish messages adressed to him.

- `description`

A description of the bot, printed when calling `help`.

- `game`

Sets the "Playing" message of your bot, placed after a help command

- `extensions`

A list of all extensions the bot will automatically load after starting. You can add more members either manually or by passing `True` as second argument to `load <ext>`

- `maintainer`

ID of the user with privileges to maintain the bot. Only this user can load, unload and reload extensions. 

##### server.json
*You can either edit this file manually or use the respective moderation commands.*

As soon as the bot joins a server, it will fill `server.json` automatically with an dictionary identified by the server ID with the following keys: 

- `adminRole`

Everyone with the given role has the permissions to run admin commands of the bot

- `modRole`

Everyone with the given role has the permissions to run mod commands of the bot

- `joinMessage`

A Message every user gets when he joins your server.

- `suggestionChannel`

A designated channel for the bot's suggest function. See `help suggest` for more informations

- `modChannel`

A channel the bot is using for logging moderation commands.



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