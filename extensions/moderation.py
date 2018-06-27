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

    #Logs
    async def on_member_join(self, member):
        await member.send(s[str(member.guild.id)]["joinMessage"])
        if(s[str(member.guild.id)]["modChannel"] != 0):
            e = discord.Embed(color=0x32c832)
            e.set_author(name = str(member) + " has joined the server.", icon_url=member.avatar_url)
            e.add_field(name="ID", value=str(member.id), inline=False)
            e.add_field(name="Mention", value=member.mention, inline=False)
            chan = self.bot.get_channel(s[str(member.guild.id)]["modChannel"])
            await chan.send(embed=e)

    async def on_member_remove(self, member):
        if(s[str(member.guild.id)]["modChannel"] != 0):
            e = discord.Embed(color=0xc83232)
            e.set_author(name = str(member) + " has left the server.", icon_url=member.avatar_url)
            e.add_field(name="ID", value=str(member.id), inline=False)
            e.add_field(name="Mention", value=member.mention, inline=False)
            chan = self.bot.get_channel(s[str(member.guild.id)]["modChannel"])
            await chan.send(embed=e)

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

    @mod.command()
    async def kick(self, ctx, id : int = None, *, msg : str = None):
        if(id == None):
            return await ctx.send("Missing id")
        if(msg == None):
            return await ctx.send("Please specify a reason for kicking this user")
        user = ctx.guild.get_member(id)
        if user is None:
            return await ctx.send("User not Found")
        if(s[str(ctx.guild.id)]["modRole"] in [r.name for r in user.roles]):
            return await ctx.send("You can't kick this user")
        await ctx.guild.kick(user)
        if(s[str(ctx.guild.id)]["modChannel"] != 0):
            e = discord.Embed(color=0x6428c8)
            e.set_author(name = ctx.author.name, icon_url=ctx.author.avatar_url)
            e.add_field(name="Kicked:", value=str(user), inline=False)
            e.add_field(name="Reason:", value=msg, inline=False)
            chan = self.bot.get_channel(s[str(ctx.guild.id)]["modChannel"])
            await chan.send(embed=e)

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