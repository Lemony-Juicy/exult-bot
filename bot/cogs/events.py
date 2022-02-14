from database.cases import CasesDB
from database.leveling import LevelingDB
import discord
from discord.ext import commands
import string
import random
import json
import ast

from database.ticket import TicketDB
from kimetsu import embed
from database.automod import AutoModDB
from database.prefix import PrefixDB
from database.events import EventDB
import datetime

from cogs.leveling import LevelingDbClient

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.e = embed.Embed().embed()
        self.Client = LevelingDbClient(bot)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                title="An Unexpected Error Occurred!",
                description=f"""
                ```cmd
                {error.original}
                ```
                """,
                colour=0xef534e
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="An Unexpected Error Occurred!",
                description=f"""
                ```cmd
                retry after: {error.retry_after} seconds
                ```
                """,
                colour=0xef534e
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="An Unexpected Error Occurred!",
                description=f"""
                ```cmd
                {error.message}
                ```
                """,
                colour=0xef534e
            )
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(title="New server joined!", description=f"**Server:** `{guild.name}`\n**Members:** {len(guild.members)}", colour=discord.Colour.green()).set_footer(text=f"ID: {guild.id}")
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await self.bot.get_channel(914193452428836884).send(embed=embed)

        con = PrefixDB(self.bot.db)
        await con.add(guild.id, "e!")
        
        con = EventDB(self.bot.db)
        await con.add(guild=guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(title="Removed from server!", description=f"**Server:** `{guild.name}`\n**Members:** {len(guild.members)}", colour=discord.Colour.red()).set_footer(text=f"ID: {guild.id}")
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await self.bot.get_channel(914193452428836884).send(embed=embed)
        
        con = PrefixDB(self.bot.db)
        await con.remove(guild.id)
        
        con = EventDB(self.bot.db)
        await con.remove(guild=guild.id)
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        con = PrefixDB(self.bot.db)
        prefix = await con.get(message.guild.id)
        prefix = prefix[0]
        if message.content == "<@!889185777555210281>":
            await message.reply(f"My prefix is: `{prefix}`")
        if message.content.startswith("v!") and prefix == "e!":
            await message.reply("My prefix is no longer `v!`, it is now `e!`. If you'd like to change it to something else you can do `e!config prefix <new_prefix>`!")
        if message.guild.id in [336642139381301249, 744484300694487050]:
            return
        if message.guild:
            if message.guild.id == 912148314223415316:
                await self.Client.add_xp(message.author, message)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        x = LevelingDB(self.bot.db)
        await x.insert(member.id, member.guild.id, 0, 1)

        
def setup(bot):
    bot.add_cog(Events(bot))
