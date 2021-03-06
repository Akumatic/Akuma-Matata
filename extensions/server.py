import discord, random, typing
from discord.ext import commands
from datetime import datetime

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update = {
            "allowUpdate": True,
            "url": "https://raw.github.com/Akumatic/Akuma-Matata/master/extensions/server.py",
            "private": False
        }

    def serverCfgCheck(self, id : int, key : str, default):
        change = False
        if str(id) not in self.bot.serverCfg:
            self.bot.serverCfg[str(id)] = {}
            change = True
        if "server" not in self.bot.serverCfg[str(id)]:
            self.bot.serverCfg[str(id)]["server"] = {}
            change = True
        if key not in self.bot.serverCfg[str(id)]["server"]:
            self.bot.serverCfg[str(id)]["server"][key] = default
            change = True
        if change:
            self.bot.writeJSON("server.json", self.bot.serverCfg)

    def getCheckOrX(self, b: bool):
        return ":white_check_mark:" if b else ":x:"

    async def toggleEvent(self, ctx, type: str):
        self.serverCfgCheck(ctx.guild.id, type, False)
        temp = not self.bot.serverCfg[str(ctx.guild.id)]["server"][type]
        self.bot.serverCfg[str(ctx.guild.id)]["server"][type] = temp
        self.bot.writeJSON("server.json", self.bot.serverCfg)
        e = discord.Embed(description=ctx.author.mention, color=discord.Color.green())
        e.set_author(name=f"{ctx.author.display_name} ({ctx.author})", icon_url=ctx.author.avatar_url)
        e.add_field(name=f"`{type}` successfully set to {temp}", value=self.getCheckOrX(temp))
        await ctx.send(embed=e)

    async def setChannel(self, ctx, type: str, channel : discord.TextChannel = None, idStr : str = None):
        e = discord.Embed(description=ctx.author.mention)
        e.set_author(name=f"{ctx.author.display_name} ({ctx.author})", icon_url=ctx.author.avatar_url)
        if channel is not None:
            self.serverCfgCheck(ctx.guild.id, type, 0)
            self.bot.serverCfg[str(ctx.guild.id)]["server"][type] = channel.id
            self.bot.writeJSON("server.json", self.bot.serverCfg)
            e.color = discord.Color.green()
            e.add_field(name=f"`{type}` successfully set to", value=channel.mention)
            return await ctx.send(embed=e)
        if idStr is None:
            e.color = discord.Color.red()
            e.add_field(name=f"`{type}` not set", value="Please specify a valid channel")
            return await ctx.send(embed=e)
        try: 
            id = int(idStr)
        except:
            e.color = discord.Color.red()
            e.add_field(name=f"`{type}` not set", value="Please specify a valid channel")
            return await ctx.send(embed=e)
        if id not in [c.id for c in ctx.guild.channels]:
            e.color = discord.Color.red()
            e.add_field(name="Channel not found", value=f"Channel {id} does not exist on this server.")
            return await ctx.send(embed=e)
        self.serverCfgCheck(ctx.guild.id, type, 0)
        self.bot.serverCfg[str(ctx.guild.id)]["server"][type] = id
        self.bot.writeJSON("server.json", self.bot.serverCfg)
        e.color = discord.Color.green()
        e.add_field(name=f"`{type}` successfully set to", value=self.bot.get_channel(id).mention)
        await ctx.send(embed=e)

    async def resetChannel(self, ctx, type: str):
        self.serverCfgCheck(ctx.guild.id, type, 0)
        self.bot.serverCfg[str(ctx.guild.id)]["server"][type] = 0
        self.bot.writeJSON("server.json", self.bot.serverCfg)
        e = discord.Embed(description=ctx.author.mention)
        e.set_author(name=f"{ctx.author.display_name} ({ctx.author})", icon_url=ctx.author.avatar_url)
        e.add_field(name=f"`{type}`", value="has been successfully reset")
        e.color = discord.Color.green()
        await ctx.send(embed=e)

    async def channelNotSpecified(self, event: str, flag: str, channel: str, setChannelCmd:str, toggleCmd: str, guild):
        if self.bot.serverCfg[str(guild.id)]["server"]["modChannel"] != 0:
            e = discord.Embed(title=f"<< {event} Event >>", color=discord.Color.red())
            e.add_field(inline=False, name=f"The `{flag}` flag is set ...", 
                value=f"but no `{channel}` was specified.")
            e.add_field(name="You can set it up with",
                value=f"`{self.bot.command_prefix}{setChannelCmd}`")
            e.add_field(name="You can disable it with",
                value=f"`{self.bot.command_prefix}{toggleCmd}`")
            chan = self.bot.get_channel(self.bot.serverCfg[str(guild.id)]["server"]["modChannel"])
            await chan.send(embed=e)
        else:
            e = discord.Embed(title="<< Member Join Event >>", color=discord.Color.red())
            e.add_field(inline=False, name=f"The `{flag}` flag in **{guild.name}** is set ...", 
                value=f"but no `{channel}` was specified.")
            e.add_field(name="You can set it up with",
                value=f"`{self.bot.command_prefix}{setChannelCmd}`")
            e.add_field(name="You can disable it with",
                value=f"`{self.bot.command_prefix}{toggleCmd}`")
            e.add_field(name="You received this message directly because no `modChannel` was specified. You can"
                " set it up with", value=f"`{self.bot.command_prefix}setModChannel`")
            user = guild.owner
            await user.send(embed=e)

    #Listener
    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.serverCfgCheck(member.guild.id, "logMemberEvent", False)
        self.serverCfgCheck(member.guild.id, "joinMessage", "")
        self.serverCfgCheck(member.guild.id, "memberEventChannel", 0)
        self.serverCfgCheck(member.guild.id, "modChannel", 0)

        if self.bot.serverCfg[str(member.guild.id)]["server"]["logMemberEvent"]:
            try:
                if self.bot.serverCfg[str(member.guild.id)]["server"]["joinMessage"] != "":
                    await member.send(self.bot.serverCfg[str(member.guild.id)]["server"]["joinMessage"])
            except discord.errors.Forbidden:
                pass
            if self.bot.serverCfg[str(member.guild.id)]["server"]["memberEventChannel"] != 0:
                e = discord.Embed(title="<< Member Join Event >>", color=discord.Color.green())
                e.set_author(name=f"{member} joined the server.", icon_url=member.avatar_url)
                e.add_field(name="ID", value=f"{member.id}", inline=False)
                e.add_field(name="Mention", value=member.mention, inline=False)
                chan = self.bot.get_channel(self.bot.serverCfg[str(member.guild.id)]["server"]["memberEventChannel"])
                await chan.send(embed=e)
            else:
                await self.channelNotSpecified("Member Join", "logMemberEvent", "memberEventChannel", 
                    "setMemberEventChannel", "toggleMemberEvent", member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.serverCfgCheck(member.guild.id, "logMemberEvent", False)
        self.serverCfgCheck(member.guild.id, "memberEventChannel", 0)
        self.serverCfgCheck(member.guild.id, "modChannel", 0)

        if self.bot.serverCfg[str(member.guild.id)]["server"]["logMemberEvent"]:
            if self.bot.serverCfg[str(member.guild.id)]["server"]["memberEventChannel"] != 0:
                e = discord.Embed(title="<< Member Leave Event >>", color=discord.Color.red())
                e.set_author(name=f"{member} left the server.", icon_url=member.avatar_url)
                e.add_field(name="ID", value=f"{member.id}", inline=False)
                e.add_field(name="Mention", value=member.mention, inline=False)
                e.add_field(name="Last known name", value=member.display_name, inline=False)
                chan = self.bot.get_channel(self.bot.serverCfg[str(member.guild.id)]["server"]["memberEventChannel"])
                await chan.send(embed=e)
            else:
                await self.channelNotSpecified("Member Leave", "logMemberEvent", "memberEventChannel", 
                    "setMemberEventChannel", "toggleMemberEvent", member.guild)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild is None or before.author.bot:
            return
        self.serverCfgCheck(before.guild.id, "logMessageEvent", False)
        self.serverCfgCheck(before.guild.id, "messageEventChannel", 0)
        self.serverCfgCheck(before.guild.id, "modChannel", 0)

        if self.bot.serverCfg[str(before.guild.id)]["server"]["logMessageEvent"] and before.content != after.content:
            if self.bot.serverCfg[str(before.guild.id)]["server"]["messageEventChannel"] != 0:
                e = discord.Embed(color=0x32c8c8, title="<< Message Edit Event >>")
                e.set_author(name=f"{before.author} edited a message.", icon_url=before.author.avatar_url)
                e.add_field(name="Profile", value=before.author.mention, inline=True)
                e.add_field(name="Channel", value=before.channel.mention, inline=True)
                e.add_field(name="URL", value=after.jump_url, inline=False)

                if len(before.content) < 1025:
                    e.add_field(name="Message before", value=before.content, inline=False)
                else:
                    e.add_field(name="Message before", value=before.content[:1024], inline=False)
                    e.add_field(name="[...]", value=before.content[1024:], inline=False)

                if len(after.content) < 1025:
                    e.add_field(name="Message after", value=after.content, inline=False)
                else:
                    e.add_field(name="Message after", value=after.content[:1024], inline=False)
                    e.add_field(name="[...]", value=after.content[1024:], inline=False)

                chan = self.bot.get_channel(self.bot.serverCfg[str(before.guild.id)]["server"]["messageEventChannel"])
                await chan.send(embed=e)
            else:
                await self.channelNotSpecified("Message Edit", "logMessageEvent", "messageEventChannel", 
                    "setMessageEventChannel", "toggleMessageEvent", before.guild)
 
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild is None or message.author.bot:
            return
        self.serverCfgCheck(message.guild.id, "logMessageEvent", False)
        self.serverCfgCheck(message.guild.id, "messageEventChannel", 0)
        self.serverCfgCheck(message.guild.id, "modChannel", 0)

        if self.bot.serverCfg[str(message.guild.id)]["server"]["logMessageEvent"]:
            if self.bot.serverCfg[str(message.guild.id)]["server"]["messageEventChannel"] != 0:
                e = discord.Embed(color=0xc83232, title="<< Message Delete Event >>")
                e.set_author(name=f"{message.author}'s message got deleted.", icon_url=message.author.avatar_url)
                e.add_field(name="Profile", value=message.author.mention, inline=True)
                e.add_field(name="Channel", value=message.channel.mention, inline=True)
                
                if message.content:
                    if len(message.content) < 1025:
                        e.add_field(name="Message", value=message.content, inline=False)
                    else:
                        e.add_field(name="Message", value=message.content[:1024], inline=False)
                        e.add_field(name="[...]", value=message.content[1024:], inline=False)
                num = len(message.attachments)
                if num > 0:
                    e.add_field(name="Attachments", value=f"The message had {num} attachment(s)", inline=False)
                    for a in message.attachments:
                        e.add_field(name="File Name", value=a.filename, inline=False)

                chan = self.bot.get_channel(self.bot.serverCfg[str(message.guild.id)]["server"]["messageEventChannel"])
                await chan.send(embed=e)
            else:
                await self.channelNotSpecified("Message Delete", "logMessageEvent", "messageEventChannel", 
                    "setMessageEventChannel", "toggleMessageEvent", message.guild)

    @commands.command()
    @commands.guild_only()
    async def greetMe(self, ctx):
        """Prints the greeting text a user receives by joining the server"""
        self.serverCfgCheck(ctx.guild.id, "joinMessage", "")
        e = discord.Embed(description=ctx.author.mention)
        e.set_author(name=f"{ctx.author.display_name} ({ctx.author})", icon_url=ctx.author.avatar_url)
        temp = self.bot.serverCfg[str(ctx.guild.id)]["server"].get("joinMessage")
        if temp == "":
            e.color = discord.Color.red()
            e.add_field(name=f"Join message of `{ctx.guild.name}`", 
                value="No welcome message specified for this server.")
        else:
            e.color = discord.Color.blue()
            e.add_field(name=f"Join message of `{ctx.guild.name}`", value=temp)
        await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setJoinMessage(self, ctx, *, msg : str = ""):
        self.serverCfgCheck(ctx.guild.id, "joinMessage", "")
        self.bot.serverCfg[str(ctx.guild.id)]["server"]["joinMessage"] = msg
        self.bot.writeJSON("server.json", self.bot.serverCfg)
        e = discord.Embed(description=ctx.author.mention, color=discord.Color.green())
        e.set_author(name=f"{ctx.author.display_name} ({ctx.author})", icon_url=ctx.author.avatar_url)
        if msg == "":
            e.add_field(name="`joinMessage` has been successfully reset", value="No message was provided.")
        else:
            e.add_field(name="`joinMessage` successfully changed to:", value=msg)
        await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def toggleMessageEvent(self, ctx):
        await self.toggleEvent(ctx, "logMessageEvent")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def toggleMemberEvent(self, ctx):
        await self.toggleEvent(ctx, "logMemberEvent")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setMessageEventChannel(self, ctx, channel : discord.TextChannel = None, idStr : str = None):
        await self.setChannel(ctx, "messageEventChannel", channel, idStr)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setMemberEventChannel(self, ctx, channel : discord.TextChannel = None, idStr : str = None):
        await self.setChannel(ctx, "memberEventChannel", channel, idStr)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setModChannel(self, ctx, channel : discord.TextChannel = None, idStr : str = None):
        await self.setChannel(ctx, "modChannel", channel, idStr)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setAnnouncementChannel(self, ctx, channel : discord.TextChannel = None, idStr : str = None):
        await self.setChannel(ctx, "announcementChannel", channel, idStr)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def resetMessageEventChannel(self, ctx):
        await self.resetChannel(ctx, "messageEventChannel")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def resetMemberEventChannel(self, ctx):
        await self.resetChannel(ctx, "memberEventChannel")    

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def resetModChannel(self, ctx):
        await self.resetChannel(ctx, "modChannel")    

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def resetAnnouncementChannel(self, ctx):
        await self.resetChannel(ctx, "announcementChannel")    

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def announce(self, ctx, *, msg : str = None):
        self.serverCfgCheck(ctx.guild.id, "announcementChannel", 0)
        self.serverCfgCheck(ctx.guild.id, "announcements", 0)
        e = discord.Embed()
        e.set_author(name=f"{ctx.author.display_name} ({ctx.author})", icon_url=ctx.author.avatar_url)
        if self.bot.serverCfg[str(ctx.guild.id)]["server"]["announcementChannel"] == 0:
            e.title = "<< Announcement >>"
            e.color = discord.Color.red()
            e.add_field(inline=False, name=f"`announcementChannel`", 
                value=f"is not set.")
            e.add_field(name="You can set it up with",
                value=f"`{self.bot.command_prefix}setAnnouncementChannel`")
            return await ctx.send(embed=e)
        if msg is None:            
            e.title = "<< Announcement >>"
            e.color = discord.Color.red()
            e.add_field(inline=False, name=f"No message given", 
                value=f"Please specify a message to announce.")
            return await ctx.send(embed=e)
        num = self.bot.serverCfg[str(ctx.guild.id)]["server"]["announcements"] + 1
        self.bot.serverCfg[str(ctx.guild.id)]["server"]["announcements"] = num
        self.bot.writeJSON("server.json", self.bot.serverCfg)
        e.title = f"<< Announcement #{num} >>"
        time = datetime.utcnow().strftime('%d.%m.%Y')
        if len(msg) < 1025:
            e.add_field(name=f"{time} (UTC)", value=msg, inline=False)
        else:
            e.add_field(name=f"{time} (UTC)", value=msg[:1024], inline=False)
            e.add_field(name="[...]", value=msg[1024:], inline=False)
        chan = self.bot.get_channel(self.bot.serverCfg[str(ctx.guild.id)]["server"]["announcementChannel"])
        await chan.send(embed=e)

    def getChannelMention(self, id: str, s: str):
        channelID = self.bot.serverCfg[id]["server"][s]
        return "Not set" if channelID == 0 else self.bot.get_channel(channelID).mention

    @commands.command()
    @commands.guild_only()
    async def serverSettings(self, ctx):
        e = discord.Embed(title="<< Server Settings >>", color=discord.Color.blue())
        e.set_thumbnail(url=ctx.guild.icon_url)
        id = str(ctx.guild.id)
        d = self.bot.serverCfg[id]["server"]

        s = ""
        channel = ["modChannel", "messageEventChannel", "memberEventChannel", "announcementChannel"]
        for c in channel:
            self.serverCfgCheck(ctx.guild.id, c, 0)
            s = "\n".join([s, f"`{c}` : {self.getChannelMention(id, c)}"])
        e.add_field(name="Channel", value=s, inline=False)

        s = ""
        flags = ["logMessageEvent", "logMemberEvent"]
        for f in flags:
            self.serverCfgCheck(ctx.guild.id, f, False)
            s = "\n".join([s, f"`{f}` : {self.getCheckOrX(d[f])}"])
        e.add_field(name="Event Flags", value=s, inline=False)

        s = ""
        other = {"# of `announcements`": ["announcements", 0]}
        for o in other:
            self.serverCfgCheck(ctx.guild.id, other[o][0], other[o][1])
            s = "\n".join([s, f"{o} : {d[other[o][0]]}"])
        e.add_field(name="Other", value=s, inline=False)

        e.add_field(name="`joinMessage`", value=d["joinMessage"] if d["joinMessage"] != "" else "Not set", inline=False)
        await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    async def serverInfo(self, ctx):
        e = discord.Embed(title="<< Server Info >>", color=discord.Color.blue(), description=ctx.guild.name)
        e.set_thumbnail(url=ctx.guild.icon_url)
        cntMember = 0
        cntBots = 0
        for m in ctx.guild.members:
            if m.bot:
                cntBots += 1
            else:
                cntMember += 1

        e.add_field(name="Guild ID", value=ctx.guild.id)
        e.add_field(name="Owner", value=ctx.guild.owner.mention)
        e.add_field(name="Created at (UTC)", value=ctx.guild.created_at.strftime("%b %d %Y - %H:%M"))
        e.add_field(name="Member Count", value=f"{cntMember} User, {cntBots} Bots")
        e.add_field(name="# of Channels", 
            value=f"{len(ctx.guild.text_channels)} Text, {len(ctx.guild.voice_channels)} Voice")
        e.add_field(name="Voice Chat Region", value=ctx.guild.region)
        e.add_field(name="Description", value=ctx.guild.description, inline=False)
        await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    async def serverIcon(self, ctx):
        e = discord.Embed(title="<< Server Icon >>", color=discord.Color.blue())
        e.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, member:typing.Union[discord.Member, str] = None):
        e = discord.Embed(title="<< Member Avatar >>")
        if member == None:
            e.description = ctx.author.mention
            e.color=discord.Color.blue()
            e.set_image(url=ctx.author.avatar_url)
        elif isinstance(member, discord.Member):
            e.description = member.mention
            e.color=discord.Color.blue()
            e.set_image(url=member.avatar_url)
        else:
            e.color=discord.Color.red()
            e.add_field(name="Member not found", value="The Member you specified does not exist on this server.")
        await ctx.send(embed=e)
        
    @commands.command()
    @commands.guild_only()
    async def iam(self, ctx, role: typing.Union[discord.Role, str] = None):
        self.serverCfgCheck(ctx.guild.id, "sar", {"default": []})
        member = ctx.guild.get_member(ctx.author.id)
        e = discord.Embed(title="<< Assign self-assignable role >>")
        if role is None:
            e.color = discord.Color.red()
            e.add_field(name="No Role", value="Please specify a role to assign.")
        elif isinstance(role, discord.Role):
            for g in self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"]:
                if role.id in self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"][g]:
                    roles = member.roles
                    if role in roles:
                        e.color = discord.Color.red()
                        e.add_field(name="Role already assigned", value=f"You have the role {role} already.")
                        return await ctx.send(embed=e)
                    e.color = discord.Color.blue()
                    if g != "default":
                        for id in self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"][g]:
                            if id != role.id:
                                r = ctx.guild.get_role(id)
                                if r in roles:
                                    roles.remove(r)
                                    e.add_field(name="Unassigned role", value=f"You don't have the role {r} anymore.",
                                        inline=False)
                    roles.append(role)
                    await member.edit(roles=roles)
                    e.add_field(name="Assigned role", value=f"You have now the role {role}.")
                    return await ctx.send(embed=e)
        else:
            e.color = discord.Color.red()
            e.add_field(name="Role does not exist", value=f"{role} does not exist on this server.")
        await ctx.send(embed=e)

    @commands.command(aliases=["iamn"])
    @commands.guild_only()
    async def iamnot(self, ctx, role: typing.Union[discord.Role, str] = None):
        self.serverCfgCheck(ctx.guild.id, "sar", {"default": []})
        member = ctx.guild.get_member(ctx.author.id)
        e = discord.Embed(title="<< Unassign self-assignable role >>")
        if role is None:
            e.color = discord.Color.red()
            e.add_field(name="No Role", value="Please specify a role to unassign.")
        elif isinstance(role, discord.Role):
            roles = member.roles
            if role in roles:
                roles.remove(role)
                await member.edit(roles=roles)
                e.color = discord.Color.blue()
                e.add_field(name="Role unassigned", value=f"You don't have the role {role} anymore.")
            else:
                e.color = discord.Color.red()
                e.add_field(name="Role not assigned", value=f"You don't have the role {role}.")
        else:
            e.color = discord.Color.red()
            e.add_field(name="Role does not exist", value=f"{role} does not exist on this server.")
        await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def asar(self, ctx, role: typing.Union[discord.Role, str] = None, exclusive: str = None):
        self.serverCfgCheck(ctx.guild.id, "sar", {"default": []})
        e = discord.Embed(title="<< Add self-assignable role >>")
        if role is None:
            e.color = discord.Color.red()
            e.add_field(name="No Role", value="Please specify a role to add.")
        elif isinstance(role, discord.Role):
            for g in self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"]:
                if role.id in self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"][g]:
                    e.color = discord.Color.red()
                    e.add_field(name="Role already in List",value=f"The specified role is already in group {g}")
                    return await ctx.send(embed=e)
            if role >= ctx.guild.get_member(self.bot.user.id).top_role:
                e.color = discord.Color.red()
                e.add_field(name="Missing Permissions", value=f"The bot's highest role is below or is {role}.")
                return await ctx.send(embed=e)
            if role < ctx.author.top_role or ctx.guild.get_member(ctx.author.id).guild_permissions.administrator:
                e.color = discord.Color.blue()
                if exclusive == None:
                    self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"]["default"].append(role.id)
                    self.bot.writeJSON("server.json", self.bot.serverCfg)
                    e.add_field(name="Successfully added", value=f"{role} added to default group")
                else:  
                    if exclusive not in self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"]:
                        self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"][exclusive] = []
                    self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"][exclusive].append(role.id)
                    e.add_field(name="Created Exclusive Group", value=f"Added Group {exclusive}", inline=True)
                    self.bot.writeJSON("server.json", self.bot.serverCfg)
                    e.add_field(name="Role added", value=f"{role} added to group {exclusive}")
            else:
                e.color = discord.Color.red()
                e.add_field(name="Missing Permissions", value="You can only add roles lower than your highest role.")
        else:
            e.color = discord.Color.red()
            e.add_field(name="Role does not exist", value=f"{role} does not exist on this server.")
        await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def rsar(self, ctx, role: typing.Union[discord.Role, str] = None):
        self.serverCfgCheck(ctx.guild.id, "sar", {"default": []})
        e = discord.Embed(title="<< Remove self-assignable role >>")
        if role is None:
            e.color = discord.Color.red()
            e.add_field(name="No Role", value="Please specify a role to remove.")
        elif isinstance(role, discord.Role):
            for g in self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"]:
                if role.id in self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"][g]:
                    self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"][g].remove(role.id)
                    e.color = discord.Color.blue()
                    e.add_field(name="Role removed", value=f"{role} removed from {g}")
                    if g != "default" and len(self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"][g]) == 0:
                        del self.bot.serverCfg[str(ctx.guild.id)]["server"]["sar"][g]
                        e.add_field(name="Group removed", value=f"{g} is empty now and got removed")
                    self.bot.writeJSON("server.json", self.bot.serverCfg)
                    return await ctx.send(embed=e)
            e.color = discord.Color.red()
            e.add_field(name="Role not self-assignable", value="The role is not self-assignable.")
        else:
            e.color = discord.Color.red()
            e.add_field(name="Role does not exist", value=f"{role} does not exist on this server.")
        await ctx.send(embed=e)
    
    @commands.command()
    @commands.guild_only()
    async def lsar(self, ctx):
        self.serverCfgCheck(ctx.guild.id, "sar", {"default": []})
        e = discord.Embed(title="<< List self-assignable role >>", color=discord.Color.blue())
        id = str(ctx.guild.id)
        if len(self.bot.serverCfg[id]["server"]["sar"]) == 1 and \
            len(self.bot.serverCfg[id]["server"]["sar"]["default"]) == 0:
            e.add_field(name="No self-assignable roles found", value="There are no self-assignable roles yet.")
        else:
            for g in self.bot.serverCfg[id]["server"]["sar"]:
                s = ", ".join(ctx.guild.get_role(x).name for x in self.bot.serverCfg[id]["server"]["sar"][g])
                if g == "default":
                    e.add_field(inline=False, name="default", value=s if s != "" else "No self-assignable roles")
                else:
                    e.add_field(inline=False, name=f"{g} (Exclusive)", value=s)
        await ctx.send(embed=e)


#Setup
def setup(bot):
    bot.add_cog(Server(bot))