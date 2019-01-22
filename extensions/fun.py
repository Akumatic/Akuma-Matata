import discord, random
from discord.ext import commands

class Fun():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Ping, Pong"""
        await ctx.send(ctx.author.mention + " Pong!")

    @commands.command()
    async def dice(self, ctx):
        """Throws a six-sided dice."""
        await ctx.send(ctx.author.mention + " You rolled a D6: " + str(random.randint(1,6)))

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