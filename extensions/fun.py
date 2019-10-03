import discord, random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Ping, Pong"""
        await ctx.send("{} Pong!".format(ctx.author.mention))

    @commands.command()
    async def dice(self, ctx, *, countstr: str = "4"):
        """Throws a four-sided dice."""
        try:
            count = int(countstr)
        except:
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description="Please enter a valid number for ``dice``"))
            return

        limit = 1000  # The limit for the amount of sides of the dice can be set here
        if count > limit:
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=f"The limit for the number of sides of the dice is {limit}. Please use a smaller number next time."))
            count = limit

        await ctx.send(embed=discord.Embed(title=f"<< Dice {count} >>", description=f"{random.randint(1, int(count))}", color=0x53ff28))
    
    @commands.command(name="8ball")
    async def magic8ball(self,ctx, *, msg : str = None):
        if msg is None:
            await ctx.send(":8ball: You need to specify a question.")
        else:
            e = discord.Embed(color=0x3296ff)
            e.set_author(name = str(ctx.author), icon_url=ctx.author.avatar_url)
            e.add_field(name=":grey_question: Question", value=msg, inline=False)
            e.add_field(name=":8ball: Answer", value=random.choice(
                ["Yes.", "As I see it, yes.", "Outlook good.", "For sure", "Without a doubt.", "It is decidedly so.", 
                "Without a doubt.", "Maybe", "Perhaps","It is uncertain", "Dont even think about it.", "Nope.", "Don't "
                "count on it.", "My sources say no.", "Outlook not so good.", "Very doubtful.", "Definitely no."]
                ), inline=False)
            await ctx.send(embed=e)
    
    @commands.command()
    async def coin(self, ctx):
        """Throws a coin."""
        await ctx.send("{} Your coin flip is {}".format(ctx.author.mention, random.choice(["Head", "Tail"])))

    @commands.command()
    async def rps(self, ctx, userChoice : str = None):
        """Play Rock, Paper, Scissors with the Bot
        Input \"r\" for Rock, \"p\" for Paper and \"s\" for Scissors"""
        if userChoice == None or str.lower(userChoice) not in ["r", "p", "s"]:
            return await ctx.send("{} Invalid input. Please enter \"r\", \"p\" or \"s\"".format(ctx.author.mention))

        botChoice = ["r", "p", "s"][random.randint(0,2)]
        if userChoice == "r" and botChoice == "p":
            await ctx.send("{} You lose".format(ctx.author.mention)) 
        elif userChoice == "p" and botChoice == "s":
            await ctx.send("{} You lose".format(ctx.author.mention))
        elif userChoice == "s" and botChoice == "r":
            await ctx.send("{} You lose".format(ctx.author.mention))
        elif userChoice == "r" and botChoice == "s":
            await ctx.send("{} You win".format(ctx.author.mention))
        elif userChoice == "p" and botChoice == "r":
            await ctx.send("{} You win".format(ctx.author.mention))
        elif userChoice == "s" and botChoice == "p":
            await ctx.send("{} You win".format(ctx.author.mention))
        else:
            await ctx.send("{} It's a tie".format(ctx.author.mention))

    @commands.command()
    async def roll(self, ctx, a : int = 0,  b : int= 100):
        """Rolls a random number between min and max.
        Default values are 0 and 100"""
        if a > b:
            temp = a
            a = b
            b = temp
        await ctx.send("{} Random roll between {} and {}: {}".format(ctx.author.mention, a, b, random.randint(a, b)))

#Setup
def setup(bot):
    bot.add_cog(Fun(bot))
