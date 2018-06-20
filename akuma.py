import json
import discord
from discord.ext import commands

#config file
c =  json.load(open("settings.json", "r"))
#The Bot itself
bot = commands.Bot(description=c["description"], command_prefix=c["prefix"])

#Function to write changed config to JSON file
def writeJSON(data):
    with open("settings.json", "w") as file:
        json.dump(data, file, indent=4)

@bot.event
async def on_ready():
    print("Bot is running!")
    game = (c["prefix"] + "help" if (c["game"] == "") else c["prefix"] + "help | " + c["game"])
    return await bot.change_presence(status=discord.Status.online,activity=discord.Game(name=game))

@bot.command(hidden=True)
async def printExt(ctx):
    """Prints out every loaded extension"""
    s = []
    for ext in bot.extensions:
        s.append(ext.split(".")[1])
    await ctx.send("Loaded extensions: " + ", ".join(s))

@bot.command(hidden=True)
async def load(ctx, ext : str = None, json : bool = False):
    """Loads a new python file from \"extension\" folder.
    
    First argument is the name of python file without .py extension.
    (Optional) If second argument is True, it will be autoloaded"""
    if(ctx.author.id != c["owner"]):
        return
    if(ext == None):
        return await ctx.send("No extension specified")
    try:
        bot.load_extension("extensions." + ext)
        await ctx.send("Loaded " + ext)
        if(json):
            c["extensions"].append(ext)
            writeJSON(c)
    except Exception as e:
        await ctx.send("Failed to load extension \"{}\": {}".format(ext, "{} ({})".format(type(e).__name__, e)))

@bot.command(hidden=True)
async def reload(ctx, ext : str = None):
    """Reloads an extension"""    
    if(ctx.author.id != c["owner"]):
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
    if(ctx.author.id != c["owner"]):
        return
    if(ext == None):
        return await ctx.send("No extension specified")
    if(("extensions." + ext) in bot.extensions):
        bot.unload_extension("extensions." + ext)
        await ctx.send("Unloaded " + ext)
        if(json):
            c["extensions"].remove(ext)
            writeJSON(c)
    else:
        await ctx.send("Extension " + ext + " not loaded")

if __name__ == "__main__":
    #loads all extensions mentioned in settings.json
    for ext in c["extensions"]:
        try:
            bot.load_extension("extensions." + ext)
        except Exception as e:
            print("Failed to load extension \"{}\": {}".format(ext, "{} ({})".format(type(e).__name__, e)))
        
    bot.run(c["token"])