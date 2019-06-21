import discord, io
from discord.ext import commands
from datetime import datetime
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

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Logs
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if s[str(member.guild.id)]["logJoinAndLeave"] == True:
            if s[str(member.guild.id)]["joinMessage"] != "":
                await member.send(s[str(member.guild.id)]["joinMessage"])
            if s[str(member.guild.id)]["logJoinAndLeaveChannel"] != 0:
                e = discord.Embed(color=0x32c832)
                e.set_author(name = str(member) + " has joined the server.", icon_url=member.avatar_url)
                e.add_field(name="ID", value=str(member.id), inline=False)
                e.add_field(name="Mention", value=member.mention, inline=False)
                chan = self.bot.get_channel(s[str(member.guild.id)]["logJoinAndLeaveChannel"])
                await chan.send(embed=e)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if s[str(member.guild.id)]["logJoinAndLeave"] == True:
            if s[str(member.guild.id)]["logJoinAndLeaveChannel"] != 0:
                e = discord.Embed(color=0xc83232)
                e.set_author(name = str(member) + " has left the server.", icon_url=member.avatar_url)
                e.add_field(name="ID", value=str(member.id), inline=False)
                e.add_field(name="Mention", value=member.mention, inline=False)
                chan = self.bot.get_channel(s[str(member.guild.id)]["logJoinAndLeaveChannel"])
                await chan.send(embed=e)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild is not None and before.author.bot == False and s[str(before.guild.id)]["logEditAndDelete"] == True:
            if s[str(before.guild.id)]["logEditAndDeleteChannel"] != 0 and before.content != after.content:
                e = discord.Embed(color=0x32c8c8)
                e.set_author(name = str(before.author) + " edited a message.", icon_url=before.author.avatar_url)
                e.add_field(name="Profile", value=before.author.mention, inline=False)
                e.add_field(name="Channel", value=str(before.channel.name), inline=False)
                e.add_field(name="Message before", value=before.content,inline=False)
                e.add_field(name="Message after", value=after.content,inline=False)
                chan = self.bot.get_channel(s[str(before.guild.id)]["logEditAndDeleteChannel"])
                await chan.send(embed=e)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild is not None and message.author.bot == False and s[str(message.guild.id)]["logEditAndDelete"] == True:
            if s[str(message.guild.id)]["logEditAndDeleteChannel"] != 0:
                e = discord.Embed(color=0xc83232)
                e.set_author(name = str(message.author) + "'s message got deleted.", icon_url=message.author.avatar_url)
                e.add_field(name="Profile", value=message.author.mention, inline=False)
                e.add_field(name="Channel", value=str(message.channel.name), inline=False)
                if message.content:
                    e.add_field(name="Message", value=message.content,inline=False)
                numAtch = len(message.attachments)
                if numAtch == 1:
                    e.add_field(name="Attachments", value="The message had " + str(numAtch) + " attachment",inline=False)
                    e.add_field(name="File Name", value=message.attachments[0].filename, inline=False)
                elif numAtch > 1:
                    e.add_field(name="Attachments", value="The message had " + str(numAtch) + " attachments",inline=False)
                    for a in message.attachments:
                        e.add_field(name="File Name", value=a.filename, inline=False)
                chan = self.bot.get_channel(s[str(message.guild.id)]["logEditAndDeleteChannel"])
                await chan.send(embed=e)

    #Groups
    @commands.group()
    async def mod(self, ctx):
        """Commands usable a Mod"""
        if s[str(ctx.guild.id)]["modRole"] not in [r.name for r in ctx.author.roles]: 
            return
        if ctx.invoked_subcommand is None:
            await ctx.send(modCommands)

    @commands.group()
    async def admin(self, ctx):
        """Commands usable by an Admin"""
        if s[str(ctx.guild.id)]["adminRole"] not in [r.name for r in ctx.author.roles]:
            return
        if ctx.invoked_subcommand is None:
            await ctx.send(adminCommands)
    
    @commands.group()
    async def owner(self, ctx):
        """Commands usable by the Owner"""
        if ctx.author.id != ctx.guild.owner.id: 
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
    async def setAnnouncementChannel(self, ctx, cid : int = None):
        if cid is None:
            return await ctx.send("Please specify a channel")
        if cid not in [c.id for c in ctx.guild.channels]:
            return await ctx.send("Channel " + cid + " does not exist")
        s[str(ctx.guild.id)]["announcementChannel"] = cid
        writeServer(s)
        await ctx.send("Announcement channel set")

    @mod.command()
    async def setModChannel(self, ctx, cid : int = None):
        if cid is None:
            return await ctx.send("Please specify a channel")
        if cid not in [c.id for c in ctx.guild.channels]:
            return await ctx.send("Channel " + cid + " does not exist")
        s[str(ctx.guild.id)]["modChannel"] = cid
        writeServer(s)
        await ctx.send("Mod channel set")

    @mod.command()
    async def setMemberLogChannel(self, ctx, cid : int = None):
        if cid is None:
            return await ctx.send("Please specify a channel")
        if cid not in [c.id for c in ctx.guild.channels]:
            return await ctx.send("Channel " + cid + " does not exist")
        s[str(ctx.guild.id)]["logJoinAndLeaveChannel"] = cid
        writeServer(s)
        await ctx.send("Member log channel set")
    
    @mod.command()
    async def setMessageChannel(self, ctx, cid : int = None):
        if cid is None:
            return await ctx.send("Please specify a channel")
        if  cid not in [c.id for c in ctx.guild.channels]:
            return await ctx.send("Channel " + cid + " does not exist")
        s[str(ctx.guild.id)]["logEditAndDeleteChannel"] = cid
        writeServer(s)
        await ctx.send("Message log channel set")

    @mod.command()
    async def changeMemberLogging(self, ctx):
        if s[str(ctx.guild.id)]["logJoinAndLeave"] == True:
            s[str(ctx.guild.id)]["logJoinAndLeave"] = False
        else:
            s[str(ctx.guild.id)]["logJoinAndLeave"] = True
        writeServer(s)
        await ctx.send("Member logging set to " + str(s[str(ctx.guild.id)]["logJoinAndLeave"]))

    @mod.command()
    async def changeMessageLogging(self, ctx):
        if s[str(ctx.guild.id)]["logEditAndDelete"] == True:
            s[str(ctx.guild.id)]["logEditAndDelete"] = False
        else:
            s[str(ctx.guild.id)]["logEditAndDelete"] = True
        writeServer(s)
        await ctx.send("Message logging set to " + str(s[str(ctx.guild.id)]["logEditAndDelete"]))

    @mod.command()
    async def kick(self, ctx, id : int = None, *, msg : str = None):
        if id == None:
            return await ctx.send("Missing id")
        if msg == None:
            return await ctx.send("Please specify a reason for kicking this user")
        user = ctx.guild.get_member(id)
        if user is None:
            return await ctx.send("User not Found")
        if s[str(ctx.guild.id)]["modRole"] in [r.name for r in user.roles]:
            return await ctx.send("You can't kick this user")
        await ctx.guild.kick(user)
        if s[str(ctx.guild.id)]["modChannel"] != 0:
            e = discord.Embed(color=0x6428c8)
            e.set_author(name = ctx.author.name, icon_url=ctx.author.avatar_url)
            e.add_field(name="Kicked:", value=str(user), inline=False)
            e.add_field(name="Reason:", value=msg, inline=False)
            chan = self.bot.get_channel(s[str(ctx.guild.id)]["modChannel"])
            await chan.send(embed=e)

    @mod.command()
    async def announce(self, ctx, *, msg):
        if s[str(ctx.guild.id)]["announcementChannel"] == 0:
            return await ctx.send("No Channel for Announcements specified. Please set it up first with \"setAnnouncementChannel\"")
        else:
            e = discord.Embed(color=0x6428c8)
            num = s[str(ctx.guild.id)]["announcements"]
            num += 1
            s[str(ctx.guild.id)]["announcements"] = num
            writeServer(s)
            e.add_field(name="#" + str(s[str(ctx.guild.id)]["announcements"]) + " - " + datetime.now().strftime("%d.%m.%Y"), value=msg, inline=False)
            chan = self.bot.get_channel(s[str(ctx.guild.id)]["announcementChannel"])
            await chan.send(embed=e)

    @mod.command()
    async def printServerSettings(self, ctx):
        e = discord.Embed(color=0x6428c8)
        for i in s[str(ctx.guild.id)].items():
            n = i[0]
            if i[1] == "":
                v = "not set"
            elif i[1] == 0:
                if i[0] == "announcements":
                    v = 0
                else:
                    v = "not set"
            else:
                v = i[1]
            e.add_field(name=n, value=v, inline=False)
        await ctx.send(embed=e)

    ### Admin Commands ###
    @admin.command()
    async def addMod(self, ctx, id : int = None):
        if id == None:
            return await ctx.send("Missing id")
        user = ctx.guild.get_member(id)
        if user is None:
            return await ctx.send("User not Found")
        #Add Mod Role to User
        if s[str(ctx.guild.id)]["modRole"] not in [r.name for r in user.roles]:
            await user.add_roles(discord.utils.get(ctx.guild.roles, name=s[str(ctx.guild.id)]["modRole"]))
            await ctx.send("User " + user.name + " was added to " + s[str(ctx.guild.id)]["modRole"])
        else:
            return await ctx.send("User " + user.name + " is already in " + s[str(ctx.guild.id)]["modRole"])

    @admin.command()
    async def rmMod(self, ctx, id : int = None):
        if id == None:
            return await ctx.send("Missing id")
        user = ctx.guild.get_member(id)
        if user is None:
            return await ctx.send("User not Found")
        if user.id == ctx.author.id:
            return await ctx.send("You can't remove yourself from Mods")
        if s[str(ctx.guild.id)]["adminRole"] in [r.name for r in user.roles] and ctx.author.id != ctx.guild.owner.id:
            return await ctx.send("You can't remove this ID")
        if s[str(ctx.guild.id)]["modRole"] in [r.name for r in user.roles]:
            await user.remove_roles(discord.utils.get(ctx.guild.roles, name=s[str(ctx.guild.id)]["modRole"]))
            await ctx.send("User " + user.name + " was removed from " + s[str(ctx.guild.id)]["modRole"])
        else:
            return await ctx.send("User " + user.name + " wasn't in " + s[str(ctx.guild.id)]["modRole"])

    ### Owner Commands ###
    @owner.command()
    async def setModRole(self, ctx, msg : str):
        if msg not in [r.name for r in ctx.guild.roles]:
            return await ctx.send("Role " + msg + " does not exist")
        s[str(ctx.guild.id)]["modRole"] = msg
        writeServer(s)
        await ctx.send("Mod role set")

    @owner.command()
    async def setAdminRole(self, ctx, msg : str):
        if msg not in [r.name for r in ctx.guild.roles]:
            return await ctx.send("Role " + msg + " does not exist")
        s[str(ctx.guild.id)]["adminRole"] = msg
        writeServer(s)
        await ctx.send("Admin role set")

    @owner.command()
    async def addAdmin(self, ctx, id : int = None):
        if id == None:
            return await ctx.send("Missing id")
        user = ctx.guild.get_member(id)
        if user is None:
            return await ctx.send("User not Found")
        #Add Admin Role to User
        if s[str(ctx.guild.id)]["adminRole"] not in [r.name for r in user.roles]:
            await user.add_roles(discord.utils.get(ctx.guild.roles, name=s[str(ctx.guild.id)]["adminRole"]))
            await ctx.send("User " + user.name + " was added to " + s[str(ctx.guild.id)]["adminRole"])
        else:
            return await ctx.send("User " + user.name + " is already in " + s[str(ctx.guild.id)]["adminRole"])
        #Add Mod Role to User
        if s[str(ctx.guild.id)]["modRole"] not in [r.name for r in user.roles]:
            await user.add_roles(discord.utils.get(ctx.guild.roles, name=s[str(ctx.guild.id)]["modRole"]))
            await ctx.send("User " + user.name + " was added to " + s[str(ctx.guild.id)]["modRole"])
        else:
            return await ctx.send("User " + user.name + " is already in " + s[str(ctx.guild.id)]["modRole"])

    @owner.command()
    async def rmAdmin(self, ctx, id : int = None):
        if id == None:
            return await ctx.send("Missing id")
        user = ctx.guild.get_member(id)
        if user is None:
            return await ctx.send("User not Found")
        if user.id == ctx.author.id:
            return await ctx.send("You can't remove yourself from Admins")
        if s[str(ctx.guild.id)]["adminRole"] in [r.name for r in user.roles]:
            await user.remove_roles(discord.utils.get(ctx.guild.roles, name=s[str(ctx.guild.id)]["adminRole"]))
            await ctx.send("User " + user.name + " was removed from " + s[str(ctx.guild.id)]["adminRole"])
        else:
            return await ctx.send("User " + user.name + " wasn't in " + s[str(ctx.guild.id)]["adminRole"])

#Setup
def setup(bot):
    bot.add_cog(Moderation(bot))