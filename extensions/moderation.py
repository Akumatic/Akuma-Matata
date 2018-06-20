import discord
from discord.ext import commands
from akuma import s, c, writeServer

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
        if (s[str(ctx.guild.id)]["modRole"] not in [r.name for r in ctx.author.roles]): 
            return
        if ctx.invoked_subcommand is None:
            await ctx.send(modCommands)

    @commands.group()
    async def admin(self, ctx):
        """Commands usable by an Admin"""
        if(s[str(ctx.guild.id)]["adminRole"] not in [r.name for r in ctx.author.roles]):
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
        s[str(ctx.guild.id)]["joinMessage"] = msg
        writeServer(s)
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
        if(s[str(ctx.guild.id)]["modRole"] not in [r.name for r in user.roles]):
            await user.add_roles(discord.utils.get(ctx.guild.roles, name=s[str(ctx.guild.id)]["modRole"]))
            await ctx.send("User " + user.name + " was added to " + s[str(ctx.guild.id)]["modRole"])
        else:
            return await ctx.send("User " + user.name + " is already in " + s[str(ctx.guild.id)]["modRole"])

    @admin.command()
    async def rmMod(self, ctx, id : int = None):
        if (id == None):
            return await ctx.send("Missing id")
        user = ctx.guild.get_member(id)
        if user is None:
            return await ctx.send("User not Found")
        if (user.id == ctx.author.id):
            return await ctx.send("You can't remove yourself from Mods")
        if(s[str(ctx.guild.id)]["adminRole"] in [r.name for r in user.roles] and ctx.author.id != ctx.guild.owner.id):
            return await ctx.send("You can't remove this ID")
        if(s[str(ctx.guild.id)]["modRole"] in [r.name for r in user.roles]):
            await user.remove_roles(discord.utils.get(ctx.guild.roles, name=s[str(ctx.guild.id)]["modRole"]))
            await ctx.send("User " + user.name + " was removed from " + s[str(ctx.guild.id)]["modRole"])
        else:
            return await ctx.send("User " + user.name + " wasn't in " + s[str(ctx.guild.id)]["modRole"])

    ### Owner Commands ###
    @owner.command()
    async def setModRole(self, ctx, msg : str):
        if(msg not in [r.name for r in ctx.guild.roles]):
            return await ctx.send("Role " + msg + " does not exist")
        s[str(ctx.guild.id)]["modRole"] = msg
        writeServer(s)
        await ctx.send("Mod role set")

    @owner.command()
    async def setAdminRole(self, ctx, msg : str):
        if(msg not in [r.name for r in ctx.guild.roles]):
            return await ctx.send("Role " + msg + " does not exist")
        s[str(ctx.guild.id)]["adminRole"] = msg
        writeServer(s)
        await ctx.send("Admin role set")

    @owner.command()
    async def addAdmin(self, ctx, id : int = None):
        if (id == None):
            return await ctx.send("Missing id")
        user = ctx.guild.get_member(id)
        if user is None:
            return await ctx.send("User not Found")
        #Add Admin Role to User
        if(s[str(ctx.guild.id)]["adminRole"] not in [r.name for r in user.roles]):
            await user.add_roles(discord.utils.get(ctx.guild.roles, name=s[str(ctx.guild.id)]["adminRole"]))
            await ctx.send("User " + user.name + " was added to " + s[str(ctx.guild.id)]["adminRole"])
        else:
            return await ctx.send("User " + user.name + " is already in " + s[str(ctx.guild.id)]["adminRole"])
        #Add Mod Role to User
        if(s[str(ctx.guild.id)]["modRole"] not in [r.name for r in user.roles]):
            await user.add_roles(discord.utils.get(ctx.guild.roles, name=s[str(ctx.guild.id)]["modRole"]))
            await ctx.send("User " + user.name + " was added to " + s[str(ctx.guild.id)]["modRole"])
        else:
            return await ctx.send("User " + user.name + " is already in " + s[str(ctx.guild.id)]["modRole"])

    @owner.command()
    async def rmAdmin(self, ctx, id : int = None):
        if (id == None):
            return await ctx.send("Missing id")
        user = ctx.guild.get_member(id)
        if user is None:
            return await ctx.send("User not Found")
        if (user.id == ctx.author.id):
            return await ctx.send("You can't remove yourself from Admins")
        if(s[str(ctx.guild.id)]["adminRole"] in [r.name for r in user.roles]):
            await user.remove_roles(discord.utils.get(ctx.guild.roles, name=s[str(ctx.guild.id)]["adminRole"]))
            await ctx.send("User " + user.name + " was removed from " + s[str(ctx.guild.id)]["adminRole"])
        else:
            return await ctx.send("User " + user.name + " wasn't in " + s[str(ctx.guild.id)]["adminRole"])

#Setup
def setup(bot):
    bot.add_cog(Moderation(bot))