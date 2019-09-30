import discord, random
from discord.ext import commands
from datetime import datetime

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def serverCfgCheck(self, id : int, key : str, default):
        if str(id) not in self.bot.serverCfg:
            self.bot.serverCfg[str(id)] = {}
        if "server" not in self.bot.serverCfg[str(id)]:
            self.bot.serverCfg[str(id)]["server"] = {}
        if key not in self.bot.serverCfg[str(id)]["server"]:
            self.bot.serverCfg[str(id)]["server"][key] = default
        self.bot.writeJSON("server.json", self.bot.serverCfg)

    #Listener
    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.serverCfgCheck(member.guild.id, "logMemberEvent", False)
        self.serverCfgCheck(member.guild.id, "joinMessage", "")
        self.serverCfgCheck(member.guild.id, "memberEventChannel", 0)
        self.serverCfgCheck(member.guild.id, "modChannel", 0)

        if self.bot.serverCfg[str(member.guild.id)]["server"]["logMemberEvent"]:
            if self.bot.serverCfg[str(member.guild.id)]["server"]["joinMessage"] != "":
                await member.send(self.bot.serverCfg[str(member.guild.id)]["server"]["joinMessage"])
            if self.bot.serverCfg[str(member.guild.id)]["server"]["memberEventChannel"] != 0:
                e = discord.Embed(color=0x32c832)
                e.set_author(name = str(member) + " joined the server.", icon_url=member.avatar_url)
                e.add_field(name="ID", value=str(member.id), inline=False)
                e.add_field(name="Mention", value=member.mention, inline=False)
                chan = self.bot.get_channel(self.bot.serverCfg[str(member.guild.id)]["server"]["memberEventChannel"])
                await chan.send(embed=e)
            else:
                if self.bot.serverCfg[str(member.guild.id)]["server"]["modChannel"] != 0:
                    chan = self.bot.get_channel(self.bot.serverCfg[str(member.guild.id)]["server"]["modChannel"])
                    await chan.send("The ***logMemberEvent*** flag is set, but no ***memberEventChannel*** was specifie"
                    "d. You can set it with `{0}setMemberEventChannel <id>` or disable ***logMemberEvent*** with `{0}to"
                    "ggleMemberEvent`".format(self.bot.command_prefix))
                else:
                    user = member.guild.owner
                    await user.send("The ***logMemberEvent*** flag in your server \"{0}\" is set, but no ***memberEvent"
                    "Channel*** was specified. You can set it with `{1}setMemberEventChannel <id>` or disable ***logMem"
                    "berEvent*** with `{1}toggleMemberEvent`.\nYou received this message directly because no ***modChan"
                    "nel*** was specified. You can set it with `{1}setModChannel <id>`".format(member.guild.name, 
                    self.bot.command_prefix))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.serverCfgCheck(member.guild.id, "logMemberEvent", False)
        self.serverCfgCheck(member.guild.id, "memberEventChannel", 0)
        self.serverCfgCheck(member.guild.id, "modChannel", 0)

        if self.bot.serverCfg[str(member.guild.id)]["server"]["logMemberEvent"]:
            if self.bot.serverCfg[str(member.guild.id)]["server"]["memberEventChannel"] != 0:
                e = discord.Embed(color=0xc83232)
                e.set_author(name = str(member) + " left the server.", icon_url=member.avatar_url)
                e.add_field(name="ID", value=str(member.id), inline=False)
                e.add_field(name="Mention", value=member.mention, inline=False)
                chan = self.bot.get_channel(self.bot.serverCfg[str(member.guild.id)]["server"]["memberEventChannel"])
                await chan.send(embed=e)
            else:
                if self.bot.serverCfg[str(member.guild.id)]["server"]["modChannel"] != 0:
                    chan = self.bot.get_channel(self.bot.serverCfg[str(member.guild.id)]["server"]["modChannel"])
                    await chan.send("The ***logMemberEvent*** flag is set, but no ***memberEventChannel*** was specifie"
                    "d. You can set it with `{0}setMemberEventChannel <id>` or disable ***logMemberEvent*** with `{0}to"
                    "ggleMemberEvent`".format(self.bot.command_prefix))
                else:
                    user = member.guild.owner
                    await user.send("The ***logMemberEvent*** flag in your server \"{0}\" is set, but no ***memberEvent"
                    "Channel*** was specified. You can set it with `{1}setMemberEventChannel <id>` or disable ***logMem"
                    "berEvent*** with `{1}toggleMemberEvent`.\nYou received this message directly because no ***modChan"
                    "nel*** was specified. You can set it with `{1}setModChannel <id>`".format(member.guild.name, 
                    self.bot.command_prefix))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild is None or before.author.bot:
            return
        self.serverCfgCheck(before.guild.id, "logMessageEvent", False)
        self.serverCfgCheck(before.guild.id, "messageEventChannel", 0)
        self.serverCfgCheck(before.guild.id, "modChannel", 0)

        if self.bot.serverCfg[str(before.guild.id)]["server"]["logMessageEvent"] and before.content != after.content:
            if self.bot.serverCfg[str(before.guild.id)]["server"]["messageEventChannel"] != 0:
                e = discord.Embed(color=0x32c8c8)
                e.set_author(name = str(before.author) + " edited a message.", icon_url=before.author.avatar_url)
                e.add_field(name="Profile", value=before.author.mention, inline=False)
                e.add_field(name="Channel", value=str(before.channel.name), inline=False)
                e.add_field(name="Message before", value=before.content,inline=False)
                e.add_field(name="Message after", value=after.content,inline=False)
                chan = self.bot.get_channel(self.bot.serverCfg[str(before.guild.id)]["server"]["messageEventChannel"])
                await chan.send(embed=e)
            else:
                if self.bot.serverCfg[str(before.guild.id)]["server"]["modChannel"] != 0:
                    chan = self.bot.get_channel(self.bot.serverCfg[str(before.guild.id)]["server"]["modChannel"])
                    await chan.send("The ***logMessageEvent*** flag is set, but no ***messageEventChannel*** was specif"
                    "ied. You can set it with `{0}setMessageEventChannel <id>` or disable ***logMessageEvent*** with `"
                    "{0}toggleMessageEvent`".format(self.bot.command_prefix))
                else:
                    user = before.guild.owner
                    await user.send("The ***logMessageEvent*** flag in your server \"{0}\" is set, but no ***messageEve"
                    "ntChannel*** was specified. You can set it with `{1}setMessageEventChannel <id>` or disable ***log"
                    "MessageEvent*** with `{1}toggleMessageEvent`.\nYou received this message directly because no ***mo"
                    "dChannel*** was specified. You can set it with `{1}setModChannel <id>`".format(before.guild.name, 
                    self.bot.command_prefix))
 
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild is None or message.author.bot:
            return
        self.serverCfgCheck(message.guild.id, "logMessageEvent", False)
        self.serverCfgCheck(message.guild.id, "messageEventChannel", 0)
        self.serverCfgCheck(message.guild.id, "modChannel", 0)

        if self.bot.serverCfg[str(message.guild.id)]["server"]["logMessageEvent"]:
            if self.bot.serverCfg[str(message.guild.id)]["server"]["messageEventChannel"] != 0:
                e = discord.Embed(color=0xc83232)
                e.set_author(name = str(message.author) + "'s message got deleted.", icon_url=message.author.avatar_url)
                e.add_field(name="Profile", value=message.author.mention, inline=False)
                e.add_field(name="Channel", value=str(message.channel.name), inline=False)
                if message.content:
                    e.add_field(name="Message", value=message.content,inline=False)
                num = len(message.attachments)
                if num > 0:
                    e.add_field(name="Attachments", value="The message had {} attachment(s)".format(num),inline=False)
                    for a in message.attachments:
                        e.add_field(name="File Name", value=a.filename, inline=False)
                chan = self.bot.get_channel(self.bot.serverCfg[str(message.guild.id)]["server"]["messageEventChannel"])
                await chan.send(embed=e)
            else:
                if self.bot.serverCfg[str(message.guild.id)]["server"]["modChannel"] != 0:
                    chan = self.bot.get_channel(self.bot.serverCfg[str(message.guild.id)]["server"]["modChannel"])
                    await chan.send("The ***logMessageEvent*** flag is set, but no ***messageEventChannel*** was specif"
                    "ied. You can set it with `{0}setMessageEventChannel <id>` or disable ***logMessageEvent*** with `"
                    "{0}toggleMessageEvent`".format(self.bot.command_prefix))
                else:
                    user = message.guild.owner
                    await user.send("The ***logMessageEvent*** flag in your server \"{0}\" is set, but no ***messageEve"
                    "ntChannel*** was specified. You can set it with `{1}setMessageEventChannel <id>` or disable ***log"
                    "MessageEvent*** with `{1}toggleMessageEvent`.\nYou received this message directly because no ***mo"
                    "dChannel*** was specified. You can set it with `{1}setModChannel <id>`".format(message.guild.name, 
                    self.bot.command_prefix))

    @commands.command()
    @commands.guild_only()
    async def greetMe(self, ctx):
        """Prints the greeting text a user receives by joining the server"""
        self.serverCfgCheck(ctx.guild.id, "joinMessage", "")
        temp = self.bot.serverCfg[str(ctx.guild.id)]["server"].get("joinMessage")
        await ctx.send("No welcome message specified for this server." if temp == "" else temp)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setJoinMessage(self, ctx, *, msg : str):
        self.serverCfgCheck(ctx.guild.id, "joinMessage", "")
        self.bot.serverCfg[str(ctx.guild.id)]["server"]["joinMessage"] = msg
        self.bot.writeJSON("server.json", self.bot.serverCfg)
        await ctx.send("joinMessage successfully changed to:\n{}".format(msg))

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def toggleMessageEvent(self, ctx):
        self.serverCfgCheck(ctx.guild.id, "logMessageEvent", False)
        temp = not self.bot.serverCfg[str(ctx.guild.id)]["server"]["logMessageEvent"]
        self.bot.serverCfg[str(ctx.guild.id)]["server"]["logMessageEvent"] = temp
        self.bot.writeJSON("server.json", self.bot.serverCfg)
        await ctx.send("logMessageEvent set to {}".format(temp))

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setMessageEventChannel(self, ctx, id : int = None):
        if id is None:
            return await ctx.send("Please specify a channel")
        if id not in [c.id for c in ctx.guild.channels]:
            return await ctx.send("Channel {} does not exist on this server.".format(id))
        self.serverCfgCheck(ctx.guild.id, "messageEventChannel", 0)
        self.bot.serverCfg[str(ctx.guild.id)]["server"]["messageEventChannel"] = id
        self.bot.writeJSON("server.json", self.bot.serverCfg)
        await ctx.send("messageEventChannel successfully set.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def toggleMemberEvent(self, ctx):
        self.serverCfgCheck(ctx.guild.id, "logMemberEvent", False)
        temp = not self.bot.serverCfg[str(ctx.guild.id)]["server"]["logMemberEvent"]
        self.bot.serverCfg[str(ctx.guild.id)]["server"]["logMemberEvent"] = temp
        self.bot.writeJSON("server.json", self.bot.serverCfg)
        await ctx.send("logMemberEvent set to {}".format(temp))


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setMemberEventChannel(self, ctx, id : int = None):
        if id is None:
            return await ctx.send("Please specify a channel")
        if id not in [c.id for c in ctx.guild.channels]:
            return await ctx.send("Channel {} does not exist on this server.".format(id))
        self.serverCfgCheck(ctx.guild.id, "memberEventChannel", 0)
        self.bot.serverCfg[str(ctx.guild.id)]["server"]["memberEventChannel"] = id
        self.bot.writeJSON("server.json", self.bot.serverCfg)
        await ctx.send("memberEventChannel successfully set.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setModChannel(self, ctx, id : int = None):
        if id is None:
            return await ctx.send("Please specify a channel")
        if id not in [c.id for c in ctx.guild.channels]:
            return await ctx.send("Channel {} does not exist on this server.".format(id))
        self.serverCfgCheck(ctx.guild.id, "modChannel", 0)
        self.bot.serverCfg[str(ctx.guild.id)]["server"]["modChannel"] = id
        self.bot.writeJSON("server.json", self.bot.serverCfg)
        await ctx.send("modChannel successfully set.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setAnnouncementChannel(self, ctx, id : int = None):
        if id is None:
            return await ctx.send("Please specify a channel")
        if id not in [c.id for c in ctx.guild.channels]:
            return await ctx.send("Channel {} does not exist on this server.".format(id))
        self.serverCfgCheck(ctx.guild.id, "announcementChannel", 0)
        self.bot.serverCfg[str(ctx.guild.id)]["server"]["announcementChannel"] = id
        self.bot.writeJSON("server.json", self.bot.serverCfg)
        await ctx.send("announcementChannel successfully set.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def announce(self, ctx, *, msg : str = None):
        self.serverCfgCheck(ctx.guild.id, "announcementChannel", 0)
        self.serverCfgCheck(ctx.guild.id, "announcements", 0)
        if self.bot.serverCfg[str(ctx.guild.id)]["server"]["announcementChannel"] == 0:
            return await ctx.send("***announcementChannel*** is not set up yet. You can set it with `{0}setAnnouncement"
            "Channel <id>`".format(self.bot.command_prefix))
        if msg is None:
            return await ctx.send("Please specify a message to announce")
        e = discord.Embed(color=0x6428c8)
        num = self.bot.serverCfg[str(ctx.guild.id)]["server"]["announcements"] + 1
        self.bot.serverCfg[str(ctx.guild.id)]["server"]["announcements"] = num
        self.bot.writeJSON("server.json", self.bot.serverCfg)
        e.add_field(name="#{} - {} (UTC)".format(num, datetime.utcnow().strftime("%d.%m.%Y")), value=msg, inline=False)
        chan = self.bot.get_channel(self.bot.serverCfg[str(ctx.guild.id)]["server"]["announcementChannel"])
        await chan.send(embed=e)
        
#Setup
def setup(bot):
    bot.add_cog(Server(bot))