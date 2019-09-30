from discord.ext import commands
import discord, io

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild != None:
            return
        if message.content[:len(self.bot.command_prefix)] != self.bot.command_prefix:
            info = await self.bot.application_info()
            user = info.owner
            if user is not None:
                e = discord.Embed(color=0x802080)
                e.set_author(name = str(message.author) + " sent a DM.", 
                    icon_url=message.author.avatar_url)
                e.add_field(name="Profile", value=message.author.mention, inline=False)
                if message.content:
                    e.add_field(name="Content", value=message.content, inline=False)
                numAtch = len(message.attachments)
                if numAtch == 0:
                    await user.send(embed=e)
                elif numAtch == 1:
                    x = io.BytesIO()
                    await message.attachments[0].save(x)
                    name = message.attachments[0].filename
                    f = discord.File(x, filename = name)
                    extention = name.split(".")[-1]
                    if extention in ["jpg", "jpeg", "png", "webp", "gif"]:
                        e.set_image(url = "attachment://"+name)
                        await user.send(embed=e, file=f)
                    else:
                        e.add_field(name="Attachment",value=name, inline=False)
                        await user.send(embed=e)
                        await user.send(file=f)
                else:
                    e.add_field(name="Attachments",value=str(numAtch)+" Attachments sent",
                        inline=False)
                    await user.send(embed=e)
                    for a in message.attachments:
                        x = io.BytesIO()
                        await a.save(x)
                        await user.send(file=discord.File(x, filename=a.filename))

    @commands.command(hidden=True)
    async def botinvite(self, ctx):
        await ctx.send("Invite this bot to your server: <https://discordapp.com/oauth2/authorize?client_id={}&scope=bot"
            "&permissions=8>\nPlease read <https://github.com/Akumatic/Akuma-Matata/blob/master/README.md> for informat"
            "ions".format(self.bot.user.id))

#Setup
def setup(bot):
    bot.add_cog(User(bot))