import discord
from discord.ext import commands

class Pool:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self, arg1, arg2):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("I can do stuff! arg1: " + arg1 + "; arg2: " + arg2)

def setup(bot):
    bot.add_cog(Pool(bot))
