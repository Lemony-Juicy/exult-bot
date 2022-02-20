import discord
from discord.ext import commands
 
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(description="sends help message", aliases=['hp'])
    async def help(self, ctx):
        return await ctx.send(embed=discord.Embed(description=f"Sorry! The help command is currently under re-development.\n\n{self.bot.arrow} For a full list of features see [here](https://github.com/andeh-py/exult-bot#exult-bot-feature-progression).\n{self.bot.arrow} For further assistance with the bot, [join here](https://exult.games/discord).", colour=self.bot.red).set_author(icon_url=self.bot.user.avatar.url, name="Exult Help"))
 
def setup(bot:commands.Bot):
    bot.add_cog(Help(bot))