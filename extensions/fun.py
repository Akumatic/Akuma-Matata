import discord, random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Ping, Pong"""
        await ctx.send(ctx.author.mention + " Pong!")

    @commands.command()
    async def d4(self, ctx):
        """Throws a four-sided dice."""
        await ctx.send(ctx.author.mention + " You rolled a D4: " + str(random.randint(1,4)))

    @commands.command()
    async def d6(self, ctx):
        """Throws a six-sided dice."""
        await ctx.send(ctx.author.mention + " You rolled a D6: " + str(random.randint(1,6)))

    @commands.command()
    async def d8(self, ctx):
        """Throws a eight-sided dice."""
        await ctx.send(ctx.author.mention + " You rolled a D8: " + str(random.randint(1,8)))

    @commands.command()
    async def d10(self, ctx):
        """Throws a eight-sided dice."""
        await ctx.send(ctx.author.mention + " You rolled a D10: " + str(random.randint(1,10)))

    @commands.command()
    async def d12(self, ctx):
        """Throws a twelve-sided dice."""
        await ctx.send(ctx.author.mention + " You rolled a D12: " + str(random.randint(1,12)))

    @commands.command()
    async def d20(self, ctx):
        """Throws a twenty-sided dice."""
        await ctx.send(ctx.author.mention + " You rolled a D20: " + str(random.randint(1,20)))

    @commands.command()
    async def d100(self, ctx):
        """Throws a hundred-sided dice."""
        await ctx.send(ctx.author.mention + " You rolled a D100: " + str(random.randint(1,100)))
    
    @commands.command()
    async def magic8ball(self,ctx, *, msg : str = None):
        if msg is None:
            await ctx.send(":8ball: You need a question")
        else:
            answers = ["Yes.", "As I see it, yes.", "Outlook good.", "For sure", 
                "Without a doubt.", "It is decidedly so.", "Without a doubt.",
                "Maybe", "Perhaps","It is uncertain", "Dont even think about it.",
                "Nope.", "Don't count on it.", "My sources say no.",
                "Outlook not so good.", "Very doubtful.", "Definitely no."]
            e = discord.Embed(color=0x3296ff)
            e.set_author(name = str(ctx.author), icon_url=ctx.author.avatar_url)
            e.add_field(name=":grey_question: Question", value=msg, inline=False)
            e.add_field(name=":8ball: Answer", value=random.choice(answers), inline=False)
            await ctx.send(embed=e)
    
    @commands.command()
    async def coin(self, ctx):
        """Throws a coin."""
        await ctx.send(ctx.author.mention + " Your coin flip is " + ("Head" if (random.random() < 0.5) else "Tail"))

    @commands.command()
    async def rps(self, ctx, userChoice : str=""):
        """Play Rock, Paper, Scissors with the Bot
        Input \"r\" for Rock, \"p\" for Paper and \"s\" for Scissors"""
        vals = ["r", "p", "s"]
        userChoice = str.lower(userChoice)
        if userChoice == "" or userChoice not in vals:
            await ctx.send(ctx.author.mention + " Invalid input. Please enter \"r\", \"p\", or \"s\"")
        else:
            botChoice = vals[random.randint(0,2)]
            if(userChoice == "r" and botChoice == "p"):
                await ctx.send(ctx.author.mention + " You lose")
            elif(userChoice == "r" and botChoice == "s"):
                await ctx.send(ctx.author.mention + " You win")
            elif(userChoice == "p" and botChoice == "r"):
                await ctx.send(ctx.author.mention + " You win")  
            elif(userChoice == "p" and botChoice == "s"):
                await ctx.send(ctx.author.mention + " You lose")  
            elif(userChoice == "s" and botChoice == "r"):
                await ctx.send(ctx.author.mention + " You lose")
            elif(userChoice == "s" and botChoice == "p"):
                await ctx.send(ctx.author.mention + " You win")
            else:
                await ctx.send(ctx.author.mention + " It's a tie")

    @commands.command()
    async def roll(self, ctx, a : int = 0,  b : int= 100):
        """Rolls a random number between min and max.
        Default values are 0 and 100"""
        if(a > b):
            temp = a
            a = b
            b = temp
        await ctx.send(ctx.author.mention + " Random roll between " + str(a) + " and " + str(b) + ": " + str(random.randint(a,b)))

#Setup
def setup(bot):
    bot.add_cog(Fun(bot))