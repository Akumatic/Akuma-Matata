from discord.ext import commands
import urllib.request, urllib.error, json, os, discord, sys

class Updater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update = {
            "allowUpdate": True,
            "url": "https://raw.github.com/Akumatic/Akuma-Matata/master/extensions/updater.py",
            "private": False
        }
        self.cfg = self.bot.loadJSON("updater.json", {"token":""})

    def updaterCfgCheck(self, key : str, default):
        if key not in self.cfg[key]:
            self.bot.serverCfg[key] = default
        self.bot.writeJSON("updater.json", self.serverCfg)

    @commands.command()
    async def setPrivateToken(self, ctx, token: str = None):
        self.updaterCfgCheck("token", "")
        e = discord.Embed(title="<< Set Private Token >>")
        if token == None:
            e.color = discord.Color.red()
            e.add_field(name="No Token given", value="Please spcify the token.")
            return await ctx.send(embed=e)
        await ctx.message.delete()
        e.color = discord.Color.green()
        self.cfg["token"] = token
        self.bot.writeJSON("updater.json", self.serverCfg)
        e.add_field(name="Token set", value="The given token was stored successfully.")
        await ctx.send(embed=e)
    
    def getRequest(self, update: dict):
        r = urllib.request.Request(update["url"])
        if update["private"]:
            r.add_header("Authorization", f"token {self.cfg['token']}")
        return r

    @commands.command()
    async def update(self, ctx):
        e = discord.Embed(title="<< Updating Modules >>")
        cog = None
        extensions = self.bot.extensions
        botRootDir = os.path.sep.join(os.path.abspath(sys.argv[0]).split(os.path.sep)[:-1])
        for ext in extensions:
            temp = ext.split(".")
            cog = self.bot.get_cog(temp[-1].capitalize())
            if cog is not None and hasattr(cog, "update"):
                if cog.update["allowUpdate"]:
                    path = f"{os.path.join(botRootDir, *temp)}.py"
                    #print(f"Comparing {path} with {cog.update['url']}")
                    try:
                        local = urllib.request.urlopen(f"file://{path}").read().decode("utf-8")
                        remote = urllib.request.urlopen(self.getRequest(cog.update)).read().decode("utf-8")
                        if local != remote:
                            self.unload(temp[-1])
                            with open(path, "w") as f:
                                f.write(remote)
                            self.load(temp[-1])
                            e.add_field(name=f"{temp[-1]}", value="Updated")
                        else:
                            e.add_field(name=f"{temp[-1]}", value="No update found")
                    except urllib.error.HTTPError as ex:
                        e.add_field(name=f"{temp[-1]}", value=f"Error {ex.code}: {ex.msg}")
                else:
                    e.add_field(name=f"{temp[-1]}", value="Update not allowed.")
        await ctx.send(embed=e)


    def load(self, ext : str):
        self.bot.load_extension("extensions." + ext)

    def unload(self, ext : str):
        self.bot.unload_extension("extensions." + ext)

#Setup
def setup(bot):
    bot.add_cog(Updater(bot))