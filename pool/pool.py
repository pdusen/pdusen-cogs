import discord, re, dice
from discord.ext import commands

class Pool:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.pattern = re.compile('^(\d*)\!?(\d)*$')
        self.bot = bot

    @commands.command()
    async def pool(self, *, arg):
        """This does stuff!"""

        match = self.pattern.match(arg)
        if not match:
            await self.bot.say("You did it wrong!")
            return

        pool_size = match.group(1)
        result = dice.roll(pool_size + 'd10s')
        await self.bot.say('Results: ' + dice.utilities.verbose_print(result))

def setup(bot):
    bot.add_cog(Pool(bot))
