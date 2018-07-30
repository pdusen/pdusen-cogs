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

        success_threshold = match.group(2) or 6

        pool_size = match.group(1)
        result = dice.roll(pool_size + 'd10s')
        result.reverse()

        await self.bot.say('Results: ' + dice.utilities.verbose_print(result))

        successes = [i for i in result if i >= success_threshold]
        failures = [i for i in result if i < success_threshold]
        await self.bot.say(str(len(successes)) + ' successes, ' + str(len(failures)) + ' failures')

def setup(bot):
    bot.add_cog(Pool(bot))
