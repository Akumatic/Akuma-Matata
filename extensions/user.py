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
    async def suggest(self, ctx, *, msg : str):
        """Makes a suggestion to the moderation team. 
        
        Planned: If there's no suggestionChannel specified, send a pm to the owner."""
        await ctx.message.delete()
        e = discord.Embed(color=0x6428c8)
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        e.add_field(name="Suggestion", value=msg)
        if(s[str(ctx.guild.id)]["suggestionChannel"] != 0):
            chan = self.bot.get_channel(s[str(ctx.guild.id)]["suggestionChannel"])
            await chan.send(embed=e)
        else:
            await ctx.send(e)

#Setup
def setup(bot):
    bot.add_cog(User(bot))