import discord
from discord.ext import commands

class Emojis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def emoji(self, ctx):
        return

    @emoji.command()
    @commands.has_permissions(manage_emojis=True)
    async def add(self, ctx, name: str, link: str):
        async with self.bot.session as ses:
            async with ses.get(link) as res:
                data = await res.read()
        e = await ctx.guild.create_custom_emoji(name=name, image=data)
        await ctx.send(embed=discord.Embed(description=f"Successfully added {e}!", colour=self.bot.red))

    @emoji.command(aliases=['rem', 'delete', 'del'])
    @commands.has_permissions(manage_emojis=True)
    async def remove(self, ctx, name: str):
        for e in ctx.guild.emojis:
            if e.name.lower() == name:
                return await e.delete(reason=f"Deleted by {ctx.author}")
        await ctx.send(embed=discord.Embed(description=f"Couldn't find emoji with name {name}.", colour=self.bot.red))

def setup(bot):
    bot.add_cog(Emojis(bot))
