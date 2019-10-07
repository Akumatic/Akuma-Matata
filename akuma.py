import json, discord, os, io
from discord.ext import commands

class Akuma(commands.Bot):
    def __init__(self):
        #storing configuration path
        self.cfgPath = os.path.join(
            os.environ.get("APPDATA") or
            os.environ.get("XDG_CONFIG_HOME") or
            os.path.join(os.environ["HOME"], ".config"),
            "Akumatic", "Akuma-Matata")
            
        #creating config directory if not available
        if not os.path.exists(self.cfgPath):
            os.makedirs(self.cfgPath)
            
        #configuration objects for internal use
        self.cfg = self.loadJSON("settings.json", {"token": "", "prefix": ">>", "description": "A Discord Bot written b"
            "y Akuma#7346", "game": "", "extensions": ["core", "server", "fun", "user", "updater"]})
        if self.cfg["token"] == "":
            self.cfg["token"] = input("Please insert the Bot Token: ")
            self.writeJSON("settings.json", self.cfg)

        self.serverCfg = self.loadJSON("server.json")
        
        #initializing the bot
        super().__init__(description=self.cfg["description"], command_prefix=self.cfg["prefix"],
            case_insensitive=True)
        
        #loading extensions given in cfg
        for ext in self.cfg["extensions"]:
            try:
                self.load_extension(f"extensions.{ext}")
            except Exception as e:
                print(f"Failed to load extension '{ext}': {f'{type(e).__name__} ({e})'}")
        
    def run(self):
        super().run(self.cfg["token"])
        print("Bot stopped")
        
    def loadJSON(self, s : str, default : dict = None):
        if not os.path.isfile(os.path.join(self.cfgPath, s)):
            with open(os.path.join(self.cfgPath, s), "w+") as f:
                if default == None:
                    json.dump({}, f, indent=4)
                else:
                    json.dump(default, f, indent=4)
        with open(os.path.join(self.cfgPath, s), "r") as f:
            return json.load(f)

    def writeJSON(self, s : str, data):
        with open(os.path.join(self.cfgPath, s), "w") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    bot = Akuma()
    bot.run()