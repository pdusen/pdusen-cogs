import discord, re, dice
from collections import deque
from discord.ext import commands

class Pool:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.pattern = re.compile('^(\d*)\!?(\d*)$')
        self.bot = bot

    @commands.command(pass_context=True)
    async def dice(self, ctx, *, arg):
        """This rolls dice normally"""
        result = dice.roll(arg)

        output_strings = []
        output_strings.append('Dice roll called by ')
        output_strings.append(ctx.message.author.name)
        output_strings.append('.\n')
        output_strings.append('Result: {}'.format(str(result)))

    @commands.command(pass_context=True)
    async def pool(self, ctx, *, arg):
        """This does stuff!"""
        match = self.pattern.match(arg)
        if not match:
            await self.bot.say("You did it wrong!")
            return

        output_strings = []
        output_strings.append('Dice roll called by ')
        output_strings.append(ctx.message.author.name)
        output_strings.append('.\n')

        success_threshold = 6
        if match.group(2):
            success_threshold = int(match.group(2))

        pool_size = match.group(1) 

        if int(pool_size) > 50:
            await self.bot.say('ERROR: Invalid dice pool size; the maximum is 50!')
            return

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

        output_strings.append('  '.join(string_bits))
        output_strings.append('\n');

        remaining_successes_count = len(remaining_successes)

        if one_count > 0 and success_count == 0:
            output_strings.append('```diff\n- B O T C H E D -\n```')
        elif successes_remaining == 0:
            output_strings.append('```css\n[ FAILED ({}) ]\n```'.format(remaining_successes_count))
        elif successes_remaining >= 5:
            output_strings.append('```asciidoc\n= P H E N O M I N A L   S U C C E S S  ({}) =\n```'.format(remaining_successes_count))
        elif successes_remaining == 4:
            output_strings.append('```cs\n" EXCEPTIONAL SUCCESS ({}) "\n```'.format(remaining_successes_count))
        elif successes_remaining == 3:
            output_strings.append('```diff\n+ Complete Success ({}) +\n```'.format(remaining_successes_count))
        elif successes_remaining == 2:
            output_strings.append('```bash\n# Moderate Success ({}) #\n```'.format(remaining_successes_count))
        elif successes_remaining == 1:
            output_strings.append('```\nMarginal success... ({})\n```'.format(remaining_successes_count))

        await self.bot.say(''.join(output_strings))

def setup(bot):
    bot.add_cog(Pool(bot))
