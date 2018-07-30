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

        success_threshold = 6
        if match.group(2):
            success_threshold = int(match.group(2))

        pool_size = match.group(1)
        result = dice.roll(pool_size + 'd10s')
        result.reverse()

        await self.bot.say('Results: ' + dice.utilities.verbose_print(result))

        successes = [i for i in result if i >= success_threshold]
        failures = [i for i in result if i < success_threshold]
        ones = [i for i in result if i == 1]
        tens = [i for i in result if i == 10]

        await self.bot.say(str(len(successes)) + ' successes, ' + str(len(failures)) + ' failures')
        await self.bot.say(str(len(ones)) + ' ones, ' + str(len(tens)) + ' tens')

def setup(bot):
    bot.add_cog(Pool(bot))
