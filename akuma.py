import json, discord, io
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
    s[str(guild.id)] = {"adminRole": "", "modRole": "", "joinMessage": "", "suggestionChannel": 0, "modChannel": 0, "announcementChannel": 0, "announcements": 0, "logEditAndDelete": True, "logEditAndDeleteChannel": 0, "logJoinAndLeave": True, "logJoinAndLeaveChannel" : 0}
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

@bot.event
async def on_message(message):
    if message.guild == None and message.author.bot == False and message.content[:len(bot.command_prefix)] != bot.command_prefix:
        user = bot.get_user(c["maintainer"])
        if user is not None:
            e = discord.Embed(color=0xc83232)
            e.set_author(name = str(message.author) + " sent a DM.", icon_url=message.author.avatar_url)
            e.add_field(name="Profile", value=message.author.mention, inline=False)
            if message.content:
                e.add_field(name="Content", value=message.content, inline=False)
            numAtch = len(message.attachments)
            if numAtch == 0:
                await user.send(embed=e)
            elif numAtch == 1:
                x = io.BytesIO()
                await message.attachments[0].save(x)
                name = message.attachments[0].filename
                f = discord.File(x, filename = name)
                extention = name.split(".")[-1]
                if extention in ["jpg", "jpeg", "png", "webp", "gif"]:
                    e.set_image(url = "attachment://"+name)
                    await user.send(embed=e, file=f)
                else:
                    e.add_field(name="Attachment",value=name, inline=False)
                    await user.send(embed=e)
                    await user.send(file=f)
            else:
                e.add_field(name="Attachments",value=str(numAtch)+" Attachments sent", inline=False)
                await user.send(embed=e)
                for a in message.attachments:
                    x = io.BytesIO()
                    await a.save(x)
                    await user.send(file=discord.File(x, filename=a.filename))
    await bot.process_commands(message)

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