import discord, re, dice
from collections import deque
from discord.ext import commands

class Pool:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.pattern = re.compile('^(\d*)\!?(\d*)$')
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
        rolls = deque(result)

        one_count = sum(1 for i in rolls if i == 1)
        success_count = sum(1 for i in rolls if i >= success_threshold)

        removed_successes = []
        removed_ones = []
        remaining_successes = []
        remaining_failures = []

        while len(rolls) > 1 and rolls[0] >= success_threshold and rolls[-1] == 1:
            removed_successes.append(rolls.popleft())
            removed_ones.append(rolls.pop())

        while len(rolls) > 0 and rolls[0] >= success_threshold:
            remaining_successes.append(rolls.popleft())

        while len(rolls) > 0:
            remaining_failures.append(rolls.popleft())

        successes_remaining = len(remaining_successes)

        string_bits = []

        for roll in removed_successes:
            string_bits.append('~~{}~~'.format(roll))

        for roll in remaining_successes:
            string_bits.append('**{}**'.format(roll))

        for roll in remaining_failures:
            string_bits.append(str(roll))

        for roll in removed_ones:
            string_bits.append('~~1~~')

        await self.bot.say('  '.join(string_bits))

        if one_count > 0 and success_count == 0:
            await self.bot.say('```diff\n- B O T C H E D -\n```')
        elif successes_remaining == 0:
            await self.bot.say('```css\n[FAILED]\n```')
        elif successes_remaining >= 5:
            await self.bot.say('```asciidoc\n= P H E N O M I N A L   S U C C E S S =\n```')
        elif successes_remaining == 4:
            await self.bot.say('```cs\n" EXCEPTIONAL SUCCESS "\n```')
        elif successes_remaining == 3:
            await self.bot.say('```diff\n+ Complete Success +\n```')
        elif successes_remaining == 2:
            await self.bot.say('```bash\n# Moderate Success #\n```')
        elif successes_remaining == 1:
            await self.bot.say('```\nMarginal success...\n```')

def setup(bot):
    bot.add_cog(Pool(bot))
