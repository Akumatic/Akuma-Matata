import discord, json
from discord.ext import commands
from akuma import c, writeJSON

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
    ```"""

class Moderation():
    def __init__(self, bot):
        self.bot = bot

    #Groups
    @commands.group()
    async def mod(self, ctx):
        """Commands usable a Mod"""
        if (ctx.author.id not in c["mods"]): 
            return
        if ctx.invoked_subcommand is None:
            await ctx.send(modCommands)

    @commands.group()
    async def admin(self, ctx):
        """Commands usable by an Admin"""
        if(ctx.author.id not in c["admins"]):
            return
        if ctx.invoked_subcommand is None:
            await ctx.send(adminCommands)
    
    @commands.group()
    async def owner(self, ctx):
        """Commands usable by the Owner"""
        if (ctx.author.id != ctx.guild.owner.id): 
            return
        if ctx.invoked_subcommand is None:
            await ctx.send(ownerCommands)

    ### Mod Commands ###
    @mod.command()
    async def setJoinMessage(self, ctx, *, msg : str):
        c["joinMessage"] = msg
        writeJSON(c)
        await ctx.send("Join Message sucessfully changed to: " + msg)

    ### Admin Commands ###
    @admin.command()
    async def addMod(self, ctx, id : int = None):
        if (id == None):
            return await ctx.send("Missing id")
        user = ctx.guild.get_member(id)
        if user is None:
            return await ctx.send("User not Found")
        #Add Mod Role to User
        if(c["modRole"] not in [r.name for r in user.roles]):
            await user.add_roles(discord.utils.get(ctx.guild.roles, name=c["modRole"]))
            await ctx.send("User " + user.name + " was added to " + c["modRole"])
        else:
            return await ctx.send("User " + user.name + " is already in " + c["modRole"])

    @admin.command()
    async def rmMod(self, ctx, id : int = None):
        if (id == None):
            return await ctx.send("Missing id")
        user = ctx.guild.get_member(id)
        if user is None:
            return await ctx.send("User not Found")
        if (user.id == ctx.author.id):
            return await ctx.send("You can't remove yourself from Mods")
        if(c["adminRole"] in [r.name for r in user.roles] and ctx.author.id != ctx.guild.owner.id):
            return await ctx.send("You can't remove this ID")
        if(c["modRole"] in [r.name for r in user.roles]):
            await user.remove_roles(discord.utils.get(ctx.guild.roles, name=c["modRole"]))
            await ctx.send("User " + user.name + " was removed from " + c["modRole"])
        else:
            return await ctx.send("User " + user.name + " wasn't in " + c["modRole"])

    ### Owner Commands ###
    @owner.command()
    async def setModRole(self, ctx, msg : str):
        if(msg not in [r.name for r in ctx.guild.roles]):
            return await ctx.send("Role " + msg + " does not exist")
        c["modRole"] = msg
        writeJSON(c)
        await ctx.send("Mod role set")

    @owner.command()
    async def setAdminRole(self, ctx, msg : str):
        if(msg not in [r.name for r in ctx.guild.roles]):
            return await ctx.send("Role " + msg + " does not exist")
        c["adminRole"] = msg
        writeJSON(c)
        await ctx.send("Admin role set")

    @owner.command()
    async def addAdmin(self, ctx, id : int = None):
        if (id == None):
            return await ctx.send("Missing id")
        user = ctx.guild.get_member(id)
        if user is None:
            return await ctx.send("User not Found")
        #Add Admin Role to User
        if(c["adminRole"] not in [r.name for r in user.roles]):
            await user.add_roles(discord.utils.get(ctx.guild.roles, name=c["adminRole"]))
            await ctx.send("User " + user.name + " was added to " + c["adminRole"])
        else:
            return await ctx.send("User " + user.name + " is already in " + c["adminRole"])
        #Add Mod Role to User
        if(c["modRole"] not in [r.name for r in user.roles]):
            await user.add_roles(discord.utils.get(ctx.guild.roles, name=c["modRole"]))
            await ctx.send("User " + user.name + " was added to " + c["modRole"])
        else:
            return await ctx.send("User " + user.name + " is already in " + c["modRole"])

    @owner.command()
    async def rmAdmin(self, ctx, id : int = None):
        if (id == None):
            return await ctx.send("Missing id")
        user = ctx.guild.get_member(id)
        if user is None:
            return await ctx.send("User not Found")
        if (user.id == ctx.author.id):
            return await ctx.send("You can't remove yourself from Admins")
        if(c["adminRole"] in [r.name for r in user.roles]):
            await user.remove_roles(discord.utils.get(ctx.guild.roles, name=c["adminRole"]))
            await ctx.send("User " + user.name + " was removed from " + c["adminRole"])
        else:
            return await ctx.send("User " + user.name + " wasn't in " + c["adminRole"])

#Setup
def setup(bot):
    bot.add_cog(Moderation(bot))