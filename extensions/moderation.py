import discord, json, akuma
from discord.ext import commands

modCommands = """```Possible Commands:
    mod setJoinMessage <msg>
```"""

adminCommands = """```Possible Commands:
    admin addMod <id>
    admin rmMod <id>
```"""

ownerCommands = """```Possible Commands:
    owner addAdmin <id>
    owner rmAdmin <id>
    owner load <ext>
    owner unload <ext>
    owner reload <ext>
    ```"""

class Moderation():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def suggest(self, ctx, *, msg : str):
        """Makes a suggestion to the moderation team. 
        
        Planned: If there's no suggestionChannel specified, send a pm to the owner."""
        await ctx.message.delete()
        e = discord.Embed(color=0x6428c8)
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        e.add_field(name="Suggestion", value=msg)
        if(akuma.c["suggestionChannel"] != 0):
            chan = self.bot.get_channel(akuma.c["suggestionChannel"])
            await chan.send(embed=e)
        else:
            await ctx.send(e)

    ### Mod Commands ###
    @commands.group()
    async def mod(self, ctx):
        """Commands usable a Mod"""
        if (ctx.author.id not in akuma.c["mods"]): 
            return
        if ctx.invoked_subcommand is None:
            await ctx.send(modCommands)

    @mod.command()
    async def setJoinMessage(self, ctx, *, msg : str):
        akuma.c["joinMessage"] = msg
        akuma.writeJSON(akuma.c)
        await ctx.send("Join Message sucessfully changed to: " + msg)

    ### Admin Commands ###
    @commands.group()
    async def admin(self, ctx):
        """Commands usable by an Admin"""
        if(ctx.author.id not in akuma.c["admins"]):
            return
        if ctx.invoked_subcommand is None:
            await ctx.send(adminCommands)

    @admin.command()
    async def addMod(self, ctx, id : int = None):
        if (id == None):
            await ctx.send("Missing id")
            return
        if(id not in akuma.c["mods"]):
            akuma.c["mods"].append(id)
            akuma.writeJSON(akuma.c)
            await ctx.send("Added user id " + str(id) + " to mods")
        else:
            return await ctx.send("User is already a mod")

    @admin.command()
    async def rmMod(self, ctx, id : int = None):
        if (id == None):
            return await ctx.send("Missing id")
        if(id in akuma.c["mods"]):
            if(id in akuma.c["admins"] and ctx.author.id != akuma.c["owner"]):
                return await ctx.send("You can't remove this ID")
            else:
                akuma.c["mods"].remove(id)
                akuma.writeJSON(akuma.c)
        else:
            return await ctx.send("User wasn't an admin")

    ### Owner Commands ###
    @commands.group()
    async def owner(self, ctx):
        """Commands usable by the Owner"""
        if (ctx.author.id not in akuma.c["owner"]): 
            return
        if ctx.invoked_subcommand is None:
            await ctx.send(ownerCommands)

    @owner.command()
    async def addAdmin(self, ctx, id : int = None):
        if (id == None):
            return await ctx.send("Missing id")
        if(id not in akuma.c["admins"]):
            akuma.c["admins"].append(id)
            await ctx.send("Added user ID " + str(id) + " to admins")
        else:
            return await ctx.send("User is already an admin")
        if(id not in akuma.c["mods"]):
            akuma.c["mods"].append(id)
            await ctx.send("Added user id " + str(id) + " to mods")
        else:
            return await ctx.send("User is already a mod")
        akuma.writeJSON(akuma.c)

    @owner.command()
    async def rmAdmin(self, ctx, id : int = None):
        if (id == None):
            return await ctx.send("Missing id")
        if(id in akuma.c["admins"]):
            akuma.c["admins"].remove(id)
            akuma.writeJSON(akuma.c)
            await ctx.send("Removed user id " + str(id) + " from admins")
        else:
            return await ctx.send("User wasn't an admin")

#Setup
def setup(bot):
    bot.add_cog(Moderation(bot))