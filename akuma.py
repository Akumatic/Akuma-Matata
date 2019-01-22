import json, discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

#config files
cFile = "settings.json"
sFile = "server.json"

c = json.load(open(cFile, "r"))
s = json.load(open(sFile, "r"))
    
#Function to write changed config to JSON file
def writeConfig(data):
    json.dump(data, open(cFile, "w"), indent=4)

def writeServer(data):
    json.dump(data, open(sFile, "w"), indent=4)

#The Bot itself
bot = commands.Bot(description=c["description"], command_prefix=c["prefix"])

@bot.event
async def on_ready():
    print("Bot is running!")
    game = (c["prefix"] + "help" if (c["game"] == "") else c["prefix"] + "help | " + c["game"])
    return await bot.change_presence(status=discord.Status.online,activity=discord.Game(name=game))

@bot.event
async def on_guild_join(guild):
    s[str(guild.id)] = {"adminRole": "", "modRole": "", "joinMessage" : "", "suggestionChannel": 0, "modChannel": 0, "announcementChannel": 0, "announcements":0}
    writeServer(s)

@bot.event
async def on_guild_remove(guild):
    del s[str(guild.id)]
    writeServer(s)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@bot.command(hidden=True)
async def printExt(ctx):
    """Prints out every loaded extension"""
    string = []
    for ext in bot.extensions:
        string.append(ext.split(".")[1])
    await ctx.send("Loaded extensions: " + ", ".join(string))

@bot.command(hidden=True)
async def load(ctx, ext : str = None, json : bool = False):
    """Loads a new python file from \"extension\" folder.
    
    First argument is the name of python file without .py extension.
    (Optional) If second argument is True, it will be autoloaded"""
    if(ctx.author.id != c["maintainer"]):
        return
    if(ext == None):
        return await ctx.send("No extension specified")
    try:
        bot.load_extension("extensions." + ext)
        await ctx.send("Loaded " + ext)
        if(json):
            c["extensions"].append(ext)
            writeConfig(c)
    except Exception as e:
        await ctx.send("Failed to load extension \"{}\": {}".format(ext, "{} ({})".format(type(e).__name__, e)))

@bot.command(hidden=True)
async def reload(ctx, ext : str = None):
    """Reloads an extension"""    
    if(ctx.author.id != c["maintainer"]):
        return
    if(ext == None):
        return await ctx.send("No extension specified")
    if(("extensions." + ext) in bot.extensions):
        bot.unload_extension("extensions." + ext)
        await ctx.send("Unloaded " + ext)
        try:
            bot.load_extension("extensions." + ext)
            await ctx.send("Loaded " + ext)
        except Exception as e:
            await ctx.send("Failed to load extension \"{}\": {}".format(ext, "{} ({})".format(type(e).__name__, e)))
    else:
        await ctx.send("Extension " + ext + " not loaded")

@bot.command(hidden=True)
async def unload(ctx, ext : str = None, json : bool = False):
    """Unloads an extension. 
    
    First argument is the name of the extension.
    (Optional) If second argument is True, it will be removed from autoload"""
    if(ctx.author.id != c["maintainer"]):
        return
    if(ext == None):
        return await ctx.send("No extension specified")
    if(("extensions." + ext) in bot.extensions):
        bot.unload_extension("extensions." + ext)
        await ctx.send("Unloaded " + ext)
        if(json):
            c["extensions"].remove(ext)
            writeConfig(c)
    else:
        await ctx.send("Extension " + ext + " not loaded")

if __name__ == "__main__":
    #loads all extensions mentioned in settings.json
    if(c["token"] == ""):
        print("Please insert a Bot Token into settings.json first")
        exit()
    for ext in c["extensions"]:
        try:
            bot.load_extension("extensions." + ext)
        except Exception as e:
            print("Failed to load extension \"{}\": {}".format(ext, "{} ({})".format(type(e).__name__, e)))
        
    bot.run(c["token"])