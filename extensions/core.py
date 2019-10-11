from discord.ext import commands
import discord, io

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update = {
            "allowUpdate": True,
            "url": "https://raw.github.com/Akumatic/Akuma-Matata/master/extensions/core.py",
            "private": False
        }

    def detectSetGame(self):
        return f" | {self.bot.cfg['game']}" if self.bot.cfg["game"] != "" else ""

    #Listener
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is running!")
        game = f"{self.bot.cfg['prefix']}help{self.detectSetGame()}"
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
        e = discord.Embed(color=discord.Color.red(), title="Error")
        if isinstance(error, commands.CommandNotFound):
            #e.add_field(name="Command Not Found", value="The command you tried to use does not exist.")
            return #await ctx.author.send(embed=e)
        if isinstance(error, commands.NotOwner):
            e.add_field(name="Not The Owner", value="Only the owner of this bot can use this command.")
            return await ctx.send(embed=e)
        if isinstance(error, commands.NoPrivateMessage):
            e.add_field(name="No Direct Message", value="This command is only usable in a server.")
            return await ctx.send(embed=e)
        if isinstance(error, commands.MissingPermissions):
            e.add_field(name="Missing Permissions", value="You don't have the permissions to use this command.")
            return await ctx.send(embed=e)
        e.add_field(name="Source", value=ctx.message.channel, inline=False)
        e.add_field(name="Trigger", value=ctx.message.content, inline=False)
        e.add_field(name="Error", value=f"{type(error).__name__} ({error})", inline=False)
        await ctx.send(embed=e)

    #Commands
    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx):
        ext = self.bot.extensions
        while len(ext) > 0:
            self.bot.unload_extension(list(ext.keys())[0])
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def setGame(self, ctx, *, msg : str = None):
        self.bot.cfg["game"] = "" if msg == None else msg
        game = f"{self.bot.cfg['prefix']}help{self.detectSetGame()}"
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=game))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, ext : str = None, json : bool = False):
        """Loads a new python file from \"extension\" folder.
        
        First argument is the name of python file without .py extension.
        (Optional) If second argument is True, it will be autoloaded"""
        e = discord.Embed(title="Loading Extension")
        if ext == None:
            e.color = discord.Color.red()
            e.add_field(name="No extension specified", value="Please specify the name of the extension.")
            return await ctx.send(embed=e)
        try:
            self.bot.load_extension("extensions." + ext)
            e.color = discord.Color.green()
            e.add_field(name="Extension loaded", value=f"`{ext}` successfully loaded.", inline=False)
            if json and ext not in self.bot.cfg["extensions"]:
                self.bot.cfg["extensions"].append(ext)
                self.bot.writeJSON("settings.json", self.bot.cfg)
                e.add_field(name="Autoload", value=f"`{ext}` was added to autostart extensions.", inline=False)
        except Exception as ex:
            e.color = discord.Color.red()
            e.add_field(name=f"Failed to load extension `{ext}`", value=f"{type(ex).__name__} ({ex})")
        await ctx.send(embed=e)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, ext : str = None, json : bool = False):
        """Unloads an extension. 
        
        First argument is the name of the extension.
        (Optional) If second argument is True, it will be removed from autoload"""
        e = discord.Embed(title="Unloading Extension")
        if ext == None:
            e.color = discord.Color.red()
            e.add_field(name="No extension specified", value="Please specify the name of the extension.")
            return await ctx.send(embed=e)
        if ("extensions." + ext) in self.bot.extensions:
            self.bot.unload_extension("extensions." + ext)
            e.color = discord.Color.green()
            e.add_field(name="Extension unloaded", value=f"`{ext}` successfully unloaded.", inline=False)
            if json and ext in self.bot.cfg["extensions"]:
                self.bot.cfg["extensions"].remove(ext)
                self.bot.writeJSON("settings.json", self.bot.cfg)
                e.add_field(name="Autoload", value=f"`{ext}` was removed from autostart extensions.", inline=False)
        else:
            e.color = discord.Color.red()
            e.add_field(name=f"Failed to unload `{ext}`", value=f"`{ext}` not loaded")
        await ctx.send(embed=e)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, ext : str = None):
        """Reloads an extension""" 
        e = discord.Embed(title="Reloading Extension: Unloading")
        if ext == None:
            e.color = discord.Color.red()
            e.add_field(name="No extension specified", value="Please specify the name of the extension.")
            return await ctx.send(embed=e)

        if ("extensions." + ext) in self.bot.extensions:
            self.bot.unload_extension("extensions." + ext)
            e.color = discord.Color.green()
            e.add_field(name="Extension unloaded", value=f"`{ext}` successfully unloaded.", inline=False)
            await ctx.send(embed=e)
            e = discord.Embed(title="Reloading Extension: Loading")
            try:
                self.bot.load_extension("extensions." + ext)
                e.color = discord.Color.green()
                e.add_field(name="Extension loaded", value=f"`{ext}` successfully loaded.", inline=False)
            except Exception as ex:
                e.color = discord.Color.red()
                e.add_field(name=f"Failed to load extension `{ext}`", value=f"{type(ex).__name__} ({ex})")
        else:
            e.color = discord.Color.red()
            e.add_field(name=f"Failed to unload `{ext}`", value=f"`{ext}` not loaded")
        await ctx.send(embed=e)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def printExt(self, ctx):
        """Prints out every loaded extension"""
        string = []
        temp = None
        for ext in self.bot.extensions:
            temp = ext.split(".")
            string.append(temp[-1] if len(temp) > 1 else temp[0])
        e = discord.Embed(color=discord.Color.blue())
        e.add_field(name="Loaded extensions", value=', '.join(string))
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Core(bot))