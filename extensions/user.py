from discord.ext import commands
from akuma import s
import discord

class User():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def greetMe(self, ctx):
        """Prints the greeting text a user receives by joining the server"""
        await ctx.send(s[str(ctx.guild.id)]["joinMessage"])

    @commands.command()
    async def botinvite(self, ctx):
        await ctx.send("""Invite Link: <https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8>
        \nPlease read <https://github.com/Akumatic/Akuma-Matata/blob/master/README.md> for informations""".format(self.bot.user.id))

    @commands.command()
    async def suggest(self, ctx, *, msg : str = None):
        """Makes a suggestion to the moderation team. 

        Only callable from a server

        Your original message gets deleted and sent to a private suggestion channel.
        If no suggestion channel is specified, it will be sent to the owner instead."""
        if(ctx.guild == None):
            return await ctx.send("This command can only be used within a server")
        if(msg == None):
            return await ctx.send("Your suggestion can't be empty")
        await ctx.message.delete()
        e = discord.Embed(description="Server: " + ctx.guild.name, color=0x6428c8)
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        e.add_field(name="Suggestion", value=msg)
        if(s[str(ctx.guild.id)]["suggestionChannel"] != 0):
            chan = self.bot.get_channel(s[str(ctx.guild.id)]["suggestionChannel"])
            await chan.send(embed=e)
        else:
            await ctx.guild.get_member(ctx.guild.owner.id).send(embed=e)

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

#Setup
def setup(bot):
    bot.add_cog(User(bot))