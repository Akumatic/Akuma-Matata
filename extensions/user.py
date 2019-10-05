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
                e = discord.Embed(title="A DM forwarded by your Bot", color=discord.Color.gold())
                e.set_author(name=f"Author: {message.author}", icon_url=message.author.avatar_url)
                e.add_field(name="From", value=message.author.mention, inline=False)
                if message.content:
                    if len(message.content) < 1025:
                        e.add_field(name="Message", value=message.content, inline=False)
                    else:
                        i = 1
                        while len(message.content) > 1018:
                            e.add_field(name=f"Message ({i})", value=f"{message.content[:1019]}[...]", inline=False)
                            message.content = message.content[1019:]
                            i += 1
                        e.add_field(name=f"Message ({i})", value=f"{message.content}", inline=False)
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
                        e.set_image(url = f"attachment://{name}")
                        await user.send(embed=e, file=f)
                    else:
                        e.add_field(name="Attachment",value=name, inline=False)
                        await user.send(embed=e)
                        await user.send(file=f)
                else:
                    e.add_field(name="Attachments",value=f"{numAtch} Attachments sent",
                        inline=False)
                    await user.send(embed=e)
                    for a in message.attachments:
                        x = io.BytesIO()
                        await a.save(x)
                        await user.send(file=discord.File(x, filename=a.filename))

    @commands.command()
    async def botinvite(self, ctx):
        e = discord.Embed(title="<< Invite this bot to your server >>", description=f"[Click here to invite this bot to"
            f" your server.](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions"
            f"=8)", color=discord.Color.blue())
        e.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=e)

    @commands.command()
    async def source(self, ctx):
        e = discord.Embed(title="<< Source Code >>", description=f"[Click here to view the source code of this bot on G"
            f"ithub.](https://github.com/Akumatic/Akuma-Matata)", color=discord.Color.blue())
        e.set_thumbnail(url="https://github.githubassets.com/images/modules/logos_page/Octocat.png")
        await ctx.send(embed=e)

#Setup
def setup(bot):
    bot.add_cog(User(bot))
