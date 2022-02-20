import discord
from discord.ext import commands
import kimetsu

from datetime import datetime
from typing import Union

from database.cases import CasesDB
from database.warnings import WarningDB
from tools.components import Paginator

class Warning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = CasesDB(bot.db)

    def get_chunks(self, interval: int, array: list):
        """split up an array into a two dimensional array with the interval specified"""
        total = []
        a = 0
        if len(array) <= interval:
            return [array]
        for i in range(len(array) // interval):
            chunks = []
            for _ in range(interval):
                chunks.append(array[a])
                a += 1
            total.append(chunks)
        if len(array) % interval != 0:
            total.append(array[a:])
        return total

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx: commands.Context, member: discord.Member, reason: str):
        """Warn a member"""
        await self.db.add_case("warn", ctx.guild.id, member.id, ctx.author.id, reason, None)
        embed = discord.Embed(description=f"**Reason:** {reason}\n**Warned at:** {kimetsu.Time.parsedate(ctx.message.created_at)}", colour=self.bot.red)
        embed.set_author(icon_url=member.avatar.url, name=f"{member.name} has been warned")
        embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Warned by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warns(self, ctx, member: discord.Member=None):
        """Displays all warnings for a given member"""
        member = ctx.author if member is None else member
        member_warns = await self.db.get_cases_for_member(ctx.guild.id, member.id, "warn")
        embed = discord.Embed(colour=self.bot.red).set_author(icon_url=member.avatar.url, name=f"{member.name}'s Warnings")
        if member_warns is None or member_warns == []:
            embed.description = f"{member} has no warnings!"
            embeds = [embed]
        else:
            embeds =[]
            formatted_warns = self.get_chunks(5, member_warns)
            warn_num = 0
            for warnpage in formatted_warns:
                embed = discord.Embed(colour=self.bot.red).set_author(icon_url=member.avatar.url, name=f"{member.name}'s Warnings")
                for warn in warnpage:
                    warn_num +=1
                    last_updated = "" if not warn[7] else f"\nLast updated: {kimetsu.Time.parsedate((datetime.fromisoformat(warn[7])))}"
                    value = f"Warning ID: {warn[0]}\n" \
                            f"Warned by: {self.bot.get_user(warn[3]).mention}\n" \
                            f"Reason: {warn[5]}\n" \
                            f"Warned at: {kimetsu.Time.parsedate((datetime.fromisoformat(warn[6])))}{last_updated}"
                    embed.add_field(name=f"Warning #{warn_num}", value=value, inline=False)
                embeds.append(embed)
        if len(embeds) > 1:
            view = Paginator(ctx=ctx, pages=embeds)
        else:
            view = None
        await ctx.send(embed=embeds[0], view=view)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delwarn(self, ctx, warning_id: int):
        """Delete a warn via its ID"""
        x = await self.db.get_case(warning_id)
        if not x:
            return await ctx.send(embed=discord.Embed(description=f"Could not find a warning with an ID of `{warning_id}`", colour=self.bot.red).set_author(name="Warning not Found"))
        await self.db.remove_case(int(warning_id))
        user = self.bot.get_user(x[3])
        moderator = self.bot.get_user(x[4])
        reason = x[6]
        description = f"**User:** {user.mention}\n**Moderator:** {moderator.mention}\n**Reason:** {reason}"
        await ctx.send(embed=discord.Embed(description=description, colour=self.bot.red).set_author(icon_url=user.avatar.url, name=f"Successfully deleted warning"))

    @commands.command(aliases=['clearwarns'])
    @commands.has_permissions(manage_messages=True)
    async def delwarns(self, ctx, member: Union[discord.Member, str]):
        if isinstance(member, discord.Member):
            x = await self.db.get_cases_for_member(ctx.guild.id, member.id, "warn")
            if type(x) == list:
                total_warns = len(x)
                await self.db.clear_member(ctx.guild.id, member.id, "warn")
        elif isinstance(member, str):
            if member.lower() == "all":
                x = await self.db.clear_guild(ctx.guild.id, "warn")
            else:
                return
        if type(x) == int:
            if x <= 0:
                embed = discord.Embed(description=f"No warns logged in {ctx.guild.name}", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="No warnings found")
            else:
                embed = discord.Embed(description=f"Deleted all (`{x}`) warns for {ctx.guild.name}", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Warnings cleared")
        elif not x:
            embed = discord.Embed(description=f"Could not find any warnings for {member.mention}.", colour=self.bot.red).set_author(name="Warnings not Found")
        elif type(x) == list:
            embed=discord.Embed(description=f"Deleted {total_warns} warnings for {member.mention}", colour=self.bot.red).set_author(icon_url=member.avatar.url, name="Warnings cleared")
        await ctx.send(embed=embed)

    @commands.command()
    async def editwarn(self, ctx, warning_id: int, *, new_reason: str):
        x = await self.db.get_case(warning_id)
        if x is None:
            return await ctx.send(embed=discord.Embed(description=f"Warning `{warning_id}` does not exist!", colour=self.bot.red).set_author(name="Warning not found"))
        member = self.bot.get_user(x[3])
        moderator = self.bot.get_user(x[4])
        old_reason = x[4]
        await self.db.update_case(warning_id, new_reason)
        description = f"**Member:** {member.mention}\n" \
                      f"**Moderator:** {moderator.mention}\n" \
                      f"**Old Reason:**```\n{old_reason}\n```" \
                      f"**New Reason:**```\n{new_reason}\n```"
        await ctx.send(embed=discord.Embed(description=description, colour=self.bot.red).set_author(icon_url=member.avatar.url, name="Warning updated"))

def setup(bot):
    bot.add_cog(Warning(bot))