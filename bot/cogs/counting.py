import discord
from discord.ext import commands

from ast import literal_eval

from database.counting import countingDB

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.db = countingDB(bot.db)

    @commands.group(aliases=['count'])
    @commands.has_permissions(manage_guild=True)
    async def counting(self, ctx):
        return

    @counting.command()
    @commands.has_permissions(manage_guild=True)
    async def add(self, ctx, channel: discord.TextChannel=None):
        channel = ctx.channel if channel is None else channel
        isexisting = await self.db.get(channel.id)
        if isexisting:
            return await ctx.send(embed=discord.Embed(description=f"**{channel.mention} is already a counting channel!**", colour=self.bot.red))
        await self.db.add(channel.id)
        await ctx.send(embed=discord.Embed(description=f"**{channel.mention} is now a counting channel!**", colour=discord.Colour.green()))

    @counting.command(aliases=['stop', 'end'])
    @commands.has_permissions(manage_guild=True)
    async def remove(self, ctx, channel: discord.TextChannel=None):
        channel = ctx.channel if channel is None else channel
        isexisting = await self.db.get(channel.id)
        if isexisting:
            await self.db.remove(channel.id)
            return await ctx.send(embed=discord.Embed(description=f"**{channel.mention} is no longer a counting channel!**", colour=discord.Colour.green()))
        else:
            return await ctx.send(embed=discord.Embed(description=f"**{channel.mention} is not a counting channel!**", colour=self.bot.red))

    @counting.command(aliases=['bl'])
    @commands.has_permissions(manage_guild=True)
    async def blacklist(self, ctx, channel, member: discord.Member=None):
        if channel is None and member is None:
            channel = ctx.channel
            x = await self.db.get(channel.id)
            if x is None:
                return await ctx.send(embed=discord.Embed(description=f"**{channel.mention} is not a counting channel!", colour=self.bot.red))
            blacklisted = literal_eval(x[2])
            if len(blacklisted) < 1:
                return await ctx.send(embed=discord.Embed(description=f"**There are no members blacklisted in {channel.mention}!**", colour=self.bot.red))
            blacklistedstr = ""
            for member in blacklisted:
                blacklistedstr += f"{member.mention}\n"
            return await ctx.send(embed=discord.Embed(description=f"**Blacklisted members in <#{channel.id}>**\n\n{blacklistedstr}", colour=self.bot.red))
        if channel and member:
            if channel.startswith("<#") and channel.endswith(">"):
                channel = self.bot.get_channel(int(channel[2:-1]))
            await self.db.blacklist(channel.id, member.id)
            return await ctx.send(embed=discord.Embed(description=f"{member.mention} has been blacklisted from counting in {channel.mention}", colour=discord.Colour.green()))
        if channel and member is None:
            try:
                self.bot.get_channel(channel.id)
            except:
                if channel.startswith("<@!") and channel.endswith(">"):
                    member = ctx.guild.get_member(int(channel[3:-1]))
                channel = self.bot.get_channel(ctx.channel.id)
                await self.db.blacklist(channel.id, member.id)
                return await ctx.send(embed=discord.Embed(description=f"**{member.mention} has been blacklisted in {channel.mention}!**", colour=discord.Colour.green()))
            x = await self.db.get(channel.id)
            if x is None:
                return await ctx.send(embed=discord.Embed(description=f"**{channel.mention} is not a counting channel!", colour=self.bot.red))
            blacklisted = literal_eval(x[2])
            if len(blacklisted) < 1:
                return await ctx.send(embed=discord.Embed(description=f"**There are no members blacklisted in {channel.mention}!**", colour=self.bot.red))
            blacklistedstr = ""
            for member in blacklisted:
                blacklistedstr += f"{member.mention}\n"
            return await ctx.send(embed=discord.Embed(description=f"**Blacklisted members in <#{channel.id}>\n\n{blacklistedstr}", colour=self.bot.red))

    @counting.command(aliases=['wl'])
    @commands.has_permissions(manage_guild=True)
    async def whitelist(self, ctx, channel, member: discord.Member=None):
        if channel and member:
            x = await self.db.get(channel.id)
            if x is None or member.id not in literal_eval(x[2]):
                return await ctx.send(embed=discord.Embed(description=f"**{channel.mention} is not a counting channel!", colour=self.bot.red))
            await self.db.whitelist(channel.id, member.id)
            return await ctx.send(embed=discord.Embed(description=f"{member.mention} has been whitelisted in {channel.mention}", colour=discord.Colour.green()))
        if channel and member is None:
            try:
                self.bot.get_channel(channel.id)
                x = await self.db.get(channel.id)
                if x is None:
                    return await ctx.send(embed=discord.Embed(description=f"**{channel.mention} is not a counting channel!", colour=self.bot.red))
            except:
                if channel.startswith("<@!") and channel.endswith(">"):
                    member = ctx.guild.get_member(int(channel[3:-1]))
                channel = self.bot.get_channel(ctx.channel.id)
                x = await self.db.get(channel.id)
                if x is None or member.id not in literal_eval(x[2]):
                    return await ctx.send(embed=discord.Embed(description=f"**{channel.mention} is not a counting channel!", colour=self.bot.red))
                await self.db.whitelist(channel.id, member.id)
                return await ctx.send(embed=discord.Embed(description=f"**{member.mention} has been whitelisted in {channel.mention}!**", colour=discord.Colour.green()))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content.startswith("v!"):
            return
        x = await self.db.get(message.channel.id)
        if x is None:
            return
        number = x[0]
        lastCounted = message.guild.get_member(x[1])
        blacklist = literal_eval(x[2])
        if message.author.id in blacklist:
            return
        if message.content.isdigit():
            if message.author == lastCounted:
                await self.db.reset(message.channel.id)
                return await message.reply(embed=discord.Embed(description=f"Oops! The same person can't send 2 consecutive numbers, that's cheating! To start counting again, type 1!", colour=self.bot.red))
            numToEqual = int(number) + 1
            if int(message.content) == numToEqual:
                await message.add_reaction("✅")
                await self.db.update(message.channel.id, number+1, message.author.id)
            else:
                await message.add_reaction("❌")
                await self.db.reset(message.channel.id)
                await message.reply(embed=discord.Embed(description=f"Oh no! It seems {message.author.mention} doesn't know that `{number} + 1` is {number+1}! To start counting again, type 1!", colour=self.bot.red))
        elif "+" in message.content or "-" in message.content or "/" in message.content or "*" in message.content or "x" in message.content:
            try:
                numEntered = eval(message.content)
            except SyntaxError:
                return
            if message.author == lastCounted:
                await self.db.reset(message.channel.id)
                return await message.reply(embed=discord.Embed(description=f"Oops! The same person can't send 2 consecutive numbers, that's cheating! To start counting again, type 1!", colour=self.bot.red))
            if numEntered == number+1:
                await message.add_reaction("✅")
                await self.db.update(message.channel.id, number+1, message.author.id)
            else:
                await message.add_reaction("❌")
                await self.db.reset(message.channel.id)
                await message.reply(embed=discord.Embed(description=f"Oh no! It seems {message.author.mention} doesn't know that `{number} + 1` is {number+1}! To start counting again, type 1!", colour=self.bot.red))        

def setup(bot):
    bot.add_cog(Counting(bot))