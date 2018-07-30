import discord
from discord.ext import commands

class Pool:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self, *, arg):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("I can do stuff! arg: " + arg)

def setup(bot):
    bot.add_cog(Pool(bot))
