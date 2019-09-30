from discord.ext import commands
import discord, io

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Listener
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is running!")
        game = self.bot.cfg["prefix"] + "help" + (" | " + self.bot.cfg["game"] if self.bot.cfg["game"] != "" else "")
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=game))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.bot.serverCfg[str(guild.id)] = {}
        self.bot.writeJSON("server.json", self.bot.serverCfg)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        del self.bot.serverCfg[str(guild.id)]
        self.bot.writeJSON("server.json", self.bot.serverCfg)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return await ctx.author.send("The command you tried to use does not exist.")
        if isinstance(error, commands.NotOwner):
            return await ctx.send("Only the owner of this bot can use this command.")
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send("You don't have the necessary permissions to use this command.")
        if isinstance(error, commands.NoPrivateMessage):
            return await ctx.send("This command is only usable in a server.")
        info = await self.bot.application_info()
        user = info.owner
        if user is not None:
            e = discord.Embed(color=0xc83232)
            e.set_author(name="Error Log")
            e.add_field(name="Source", value=ctx.message.channel, inline=False)
            e.add_field(name="Trigger", value=ctx.message.content,inline=False)
            e.add_field(name="Trace", value=error, inline=False)
            await user.send(embed=e)

    #Commands
    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx):
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def changeGame(self, ctx, *, msg : str = None):
        self.bot.cfg["game"] = "" if msg == None else msg
        game = self.bot.cfg["prefix"] + "help" + (" | " + self.bot.cfg["game"] if self.bot.cfg["game"] != "" else "")
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=game))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, ext : str = None, json : bool = False):
        """Loads a new python file from \"extension\" folder.
        
        First argument is the name of python file without .py extension.
        (Optional) If second argument is True, it will be autoloaded"""
        if ext == None:
            return await ctx.send("No extension specified")
        try:
            self.bot.load_extension("extensions." + ext)
            await ctx.send("Loaded " + ext)
            if json:
                self.bot.cfg["extensions"].append(ext)
                self.bot.writeJSON("settings.json", self.bot.cfg)
        except Exception as e:
            await ctx.send("Failed to load extension \"{}\": {}".format(ext, "{} ({})".format(type(e).__name__, e)))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, ext : str = None, json : bool = False):
        """Unloads an extension. 
        
        First argument is the name of the extension.
        (Optional) If second argument is True, it will be removed from autoload"""
        if ext == None:
            return await ctx.send("No extension specified")
        if ("extensions." + ext) in self.bot.extensions:
            self.bot.unload_extension("extensions." + ext)
            await ctx.send("Unloaded " + ext)
            if json:
                self.bot.cfg["extensions"].remove(ext)
                self.bot.writeJSON("settings.json", self.bot.cfg)
        else:
            await ctx.send("Extension {} not loaded".format(ext))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, ext : str = None):
        """Reloads an extension"""    
        if ext == None:
            return await ctx.send("No extension specified")
        if ("extensions." + ext) in self.bot.extensions:
            self.bot.unload_extension("extensions." + ext)
            await ctx.send("Unloaded " + ext)
            try:
                self.bot.load_extension("extensions." + ext)
                await ctx.send("Loaded " + ext)
            except Exception as e:
                await ctx.send("Failed to load extension \"{}\": {}".format(ext, "{} ({})".format(type(e).__name__, e)))
        else:
            await ctx.send("Extension {} not loaded".format(ext))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def printExt(self, ctx):
        """Prints out every loaded extension"""
        string = []
        temp = None
        for ext in self.bot.extensions:
            temp = ext.split(".")
            string.append(temp[1] if len(temp) > 1 else temp[0])
        await ctx.send("Loaded extensions: {}".format(", ".join(string)))

def setup(bot):
    bot.add_cog(Core(bot))