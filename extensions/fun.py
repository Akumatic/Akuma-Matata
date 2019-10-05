import discord, random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Ping, Pong"""
        e = discord.Embed(title="<< Ping >>", description=ctx.author.mention, color=discord.Color.blue())
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        e.add_field(name=":ping_pong:", value="Pong!")
        await ctx.send(embed=e)

    @commands.command()
    async def dice(self, ctx, countstr: str = "6", dicesstr: str = "1"):
        """Throws a dice."""
        e = discord.Embed(description=ctx.author.mention)
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        try:
            count = int(countstr)
            dices = int(dicesstr)
        except:
            e.title="<< Dice >>"
            e.color = discord.Color.red()
            e.add_field(name=":game_die:", value="Please enter a valid number for `dice`")
            return await ctx.send(embed=e)

        limit = 120  # The limit for the amount of sides of the dice can be set here
        if count > limit:
            e.title="<< Dice >>"
            e.add_field(name=":game_die:", value=f"You tried to throw {count} sided dices. Allowed are {limit} sides.")
            e.color=discord.Color.red()
            return await ctx.send(embed=e)
        #Embed limitation
        if dices > 25:
            e.title="<< Dice >>"
            e.add_field(name=":game_die:", value=f"You tried to throw {dices} dices. Allowed are 25 dices.")
            e.color=discord.Color.red()
            return await ctx.send(embed=e)
            
        e.color = discord.Color.blue()
        e.title = f"<< {dices} Dice {count} >>"
        for i in range(dices):
            e.add_field(name=":game_die:", value = random.randint(1, count), inline=True)
        await ctx.send(embed=e)
    
    @commands.command(name="8ball")
    async def magic8ball(self, ctx, *, msg: str = None):
        e = discord.Embed(title="<< 8Ball >>", description=ctx.author.mention)
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        if msg is None:
            e.color = discord.Color.red()
            e.add_field(name=":8ball:", value="You need to specify a question.")
            return await ctx.send(embed=e)
        else:
            e.color = discord.Color.blue()
            if len(msg) < 1025:
                e.add_field(name=":grey_question: Question", value=msg, inline=False)
            else:
                e.add_field(name=":grey_question: Question", value=msg[:1024], inline=False)
                e.add_field(name="[...]", value=msg[1024:], inline=False)
            e.add_field(name=":8ball: Answer", value=random.choice(
                ["Yes.", "As I see it, yes.", "Outlook good.", "For sure", "Without a doubt.", "It is decidedly so.", 
                "Without a doubt.", "Maybe", "Perhaps","It is uncertain", "Dont even think about it.", "Nope.", "Don't "
                "count on it.", "My sources say no.", "Outlook not so good.", "Very doubtful.", "Definitely no."]
                ), inline=False)
            await ctx.send(embed=e)
    
    @commands.command()
    async def coin(self, ctx):
        """Flip a coin."""
        e = discord.Embed(title="<< Flip a coin >>", description=ctx.author.mention, color=discord.Color.blue())
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        e.add_field(name="Your coin shows ", value=f"{random.choice(['Heads', 'Tails'])}")
        await ctx.send(embed=e)

    @commands.command()
    async def rps(self, ctx, user: str = None):
        """Play Rock, Paper, Scissors with the Bot
        Input 'r' for Rock, 'p' for Paper and 's' for Scissors"""
        e = discord.Embed(title="<< Rock, Paper, Scissors >>", description=ctx.author.mention)
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        if user == None or str.lower(user) not in ["r", "p", "s"]:
            e.color=discord.Color.red()
            e.add_field(name=":moyai::newspaper::scissors:", value="Invalid input. Please use 'r', 'p' or 's'")
            return await ctx.send(embed=e)

        emote = {"r":":moyai:", "p":":newspaper:", "s":":scissors:"}
        e.color=discord.Color.blue()
        com = random.choice(["r", "p", "s"])
        e.add_field(name="You", value=emote[user], inline=True)
        e.add_field(name="Computer", value=emote[com], inline=True)
        if (user == "r" and com == "p") or (user == "p" and com == "s") or (user == "s" and com == "r"):
            e.add_field(name=":moyai::newspaper::scissors:", value="You lose")
        elif (user == "r" and com == "s") or (user == "p" and com == "r") or (user == "s" and com == "p"):
            e.add_field(name=":moyai::newspaper::scissors:", value="You win")
        else:
            e.add_field(name=":moyai::newspaper::scissors:", value="It's a tie")
        await ctx.send(embed=e)

    @commands.command()
    async def roll(self, ctx, astr: str = "0",  bstr: str = "100"):
        """Rolls a random number between min and max.
        Default values are 0 and 100"""
        e = discord.Embed(description=ctx.author.mention)
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        try:
            a = int(astr)
            b = int(bstr)
        except:
            e.title="<< Roll >>"
            e.color = discord.Color.red()
            e.add_field(name=":game_die:", value="Please enter valid numbers for `roll`")
            return await ctx.send(embed=e)

        e.color = discord.Color.blue()
        if a > b:
            temp = a
            a = b
            b = temp
        e.title = f"<< Random roll in [{a}, {b}] >>"
        e.add_field(name=":game_die:", value = random.randint(a, b))
        await ctx.send(embed=e)

#Setup
def setup(bot):
    bot.add_cog(Fun(bot))
