import discord
from discord.ext import commands
from kimetsu.time import Time

from database.suggestions import SuggestDB
from tools.components import SuggestVotes, SuggestSafeDecision


class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = SuggestDB(bot.db)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion: str):
        guildconf = await self.db.getconf(ctx.guild.id)
        if not guildconf:
            return await ctx.send(embed=discord.Embed(description=f"Oops! Seems like this server doesn't have my suggestions module enabled! To enable it, simply do `{ctx.prefix}config suggestions`!", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Config"))
        channel_id = guildconf[0]
        safemode = guildconf[1]
        await self.db.add(ctx.guild.id, ctx.message.author.id, suggestion)
        data = await self.db.get_id(ctx.guild.id, ctx.message.author.id)
        suggestion_id = data[-1][0]
        embed = discord.Embed(description=suggestion, colour=discord.Colour.gold()).set_author(icon_url=ctx.message.author.avatar.url, name=f"Suggestion from {ctx.message.author}").set_footer(icon_url=ctx.guild.icon.url, text=f"Suggsetion ID: {suggestion_id}").set_thumbnail(url=ctx.author.avatar.url)
        if safemode:
            embed.add_field(name="Suggested at", value=Time.Parsedate(discord.utils.utcnow()), inline=False)
            channel = ctx.guild.get_channel(safemode)
            view = SuggestSafeDecision(self.bot)
        else:
            embed.add_field(name="Upvotes", value="0", inline=True).add_field(name="Downvotes", value="0", inline=True).add_field(name="Total", value="0", inline=True).add_field(name="Suggested at", value=Time.Parsedate(discord.utils.utcnow()), inline=False)
            channel = ctx.guild.get_channel(channel_id)
            view = SuggestVotes(self.bot)
        msg = await channel.send(embed=embed, view=view)
        if not safemode:
            await self.db.confirm(suggestion_id, msg.id)
        embed = discord.Embed(title="Thanks for your suggestion!", description=f"Your suggestion of:\n```{suggestion}```\nhas been sent in <#{guildconf[0]}>!", colour=self.bot.red)
        await ctx.message.reply(embed=embed)

def setup(bot):
    bot.add_cog(Suggestions(bot))