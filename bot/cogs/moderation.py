import discord
from discord.ext import commands
import kimetsu

from importlib import reload
from .utils import checks, tools
from datetime import datetime
from typing import Union

from database import cases
from database import config
from tools.components import Paginator

Check = checks.Check
Embed = tools.Embed
Time = tools.Time
CasesDB = cases.CasesDB
GuildConfigDB = config.GuildConfigDB

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cdb = CasesDB(bot.db)
        self.embed = Embed(bot).embed
        reload(checks)
        reload(cases)
        reload(config)
        
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

    class ModReason(commands.Converter):
        async def convert(self, ctx, argument):
            reason = "Unspecified" if not argument else argument
            return reason
        
    class PurgeAmount(commands.Converter):
        async def convert(self, ctx, argument):
            if not argument:
                return None 
            amount = 1 if argument is None else argument
            amount = 100 if int(argument) > 100 else argument
            return int(amount)
        
    class TimeConverter(commands.Converter):
        async def convert(self, ctx, argument):
            new_time = Time.handler(argument)
            num = int(new_time[0])
            if new_time[1] in ["second", "seconds"]:
                seconds = num
            elif new_time[1] in ["minute", "minutes"]:
                seconds = num*60
            elif new_time[1] in ["hour", "hours"]:
                seconds = num*3600
            elif new_time[1] in ["day", "days"]:
                seconds = num*86400
            return [new_time, seconds]
        
    class MuteTime(commands.Converter):
        async def convert(self, ctx, argument):
            time = Time.handler(argument)
            expirationDate = Time.convert_for_command(time)
            return [time, expirationDate]
    
    @commands.command(description="ban a user")
    @Check.ban()
    #@Check.module("ban")
    async def ban(self, ctx, member: discord.Member, *, reason: ModReason=None):
        """Ban a user"""
        embed = self.embed(description=f"**Server:**{ctx.guild.name}\n**Reason:** {reason}\n**Banned at:** {Time.parsedate()}",
                           thumbnail=ctx.guild.icon.url,
                           author={"icon": member.display_avatar.url, "name": "You have been banned!"})
        try:
            await member.send(embed=embed)
        except discord.errors.Forbidden:
            pass
        if ctx.guild.id != 912148314223415316:
            await ctx.guild.ban(discord.Object(id=member.id), reason=reason)
        else:
            print(1)
            await GuildConfigDB(self.bot.db).test_reload()
        embed = self.embed(description=f"**Reason:** {reason}\n**Banned at:** {Time.parsedate()}",
                           thumbnail=member.display_avatar.url,
                           author={"icon": member.display_avatar.url, "name": f"{member} has been banned!"},
                           footer={"icon": ctx.author.display_avatar.url, "text": f"Banned by {ctx.author}"})
        await ctx.send(embed=embed)
        await self.cdb.add_case("ban", ctx.guild.id, member.id, ctx.author.id, reason, None)

    @commands.command(description="kick a user")
    @Check.kick()
    #@Check.module("kick")
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a user"""
        embed = self.embed(description=f"**Server:**{ctx.guild.name}\n**Reason:** {reason}\n**Kicked at:** {Time.parsedate()}",
                           thumbnail=ctx.guild.icon.url,
                           author={"icon": member.display_avatar.url, "name": "You have been kicked!"})
        try:
            await member.send(embed=embed)
        except discord.errors.Forbidden:
            pass
        await ctx.guild.kick(discord.Object(id=member.id), reason=reason)
        embed = self.embed(description=f"**Reason:** {reason}\n**Kicked at:** {Time.parsedate()}",
                           thumbnail=member.display_avatar.url,
                           author={"icon": member.display_avatar.url, "name": f"{member} has been kicked!"},
                           footer={"icon": ctx.author.display_avatar.url, "text": f"Kicked by {ctx.author}"})
        await ctx.send(embed=embed)
        await self.cdb.add_case("kick", ctx.guild.id, member.id, ctx.author.id, reason, None)

    @commands.command(description="unban a user")
    @Check.ban()
    #@Check.module("unban")
    async def unban(self, ctx, member: discord.User, *, reason=None):
        """Unban a user"""
        embed = self.embed(description=f"**Server:**{ctx.guild.name}\n**Reason:** {reason}\n**Unbanned at:** {Time.parsedate()}",
                           thumbnail=ctx.guild.icon.url,
                           author={"icon": member.display_avatar.url, "name": "You have been unbanned!"})
        try:
            await member.send(embed=embed)
        except discord.errors.Forbidden:
            pass
        await ctx.guild.unban(discord.Object(id=member.id), reason=reason)
        embed = self.embed(description=f"**Reason:** {reason}\n**Unbanned at:** {Time.parsedate()}",
                           thumbnail=member.display_avatar.url,
                           author={"icon": member.display_avatar.url, "name": f"{member} has been banned!"},
                           footer={"icon": ctx.author.display_avatar.url, "text": f"Banned by {ctx.author}"})
        await ctx.send(embed=embed)
        await self.cdb.add_case("unban", ctx.guild.id, member.id, ctx.author.id, reason, None)

    @commands.group(aliases=['clear'], invoke_without_command=True, description="purge messages")
    @Check.messages()
    #@Check.module("purge")
    async def purge(self, ctx, amount: PurgeAmount=None):
        """Purge messages"""
        if not amount:
            return await ctx.send(embed=discord.Embed(description=f"Please provide a number of messages to purge.", colour=self.bot.red))
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount)
        embed = Embed(self.bot).embed(title=f"Purged {len(deleted)} messages")
        await ctx.send(embed=embed, delete_after=15)

    @purge.command(description="purge messages from a member")
    @Check.messages()
    #@Check.module("purge")
    async def member(self, ctx, member: discord.Member = None, amount: PurgeAmount=None):
        """Purge messages sent by a given member"""
        if not member:
            return await ctx.send(embed=discord.Embed(description=f"Please provide a member to purge.", colour=self.bot.red))
        elif not amount:
            return await ctx.send(embed=discord.Embed(description=f"Please provide a number of messages to purge.", colour=self.bot.red))
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount, check=lambda m: m.author == member)
        embed = Embed(self.bot).embed(title=f"Purged {len(deleted)} messages from {member}")
        await ctx.send(embed=embed, delete_after=15)

    @purge.command(description="purge bot messages")
    @Check.messages()
    #@Check.module("purge")
    async def bot(self, ctx, amount: int = None):
        """Purge messages sent by bots"""
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount, check=lambda m: m.author.bot)
        embed = Embed(self.bot).embed(title=f"Purged {len(deleted)} messages from bots")
        await ctx.send(embed=embed, delete_after=15)

    @purge.command(description="purge maximum amount of messages (100)")
    @Check.messages()
    async def max(self, ctx):
        """Purge maximum amount of messages (100)"""
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=100)
        embed = Embed(self.bot).embed(title=f"Purged {len(deleted)} messages")
        await ctx.send(embed=embed, delete_after=15)

    @purge.command(description="purge after a message")
    @Check.messages()
    async def after(self, ctx, message: discord.Message, amount: PurgeAmount=None):
        """Delete messages after a given message id"""
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount, after=message)
        embed = Embed(self.bot).embed(title=f"Purged {len(deleted)} messages after [message]{message.jump_url}")
        await ctx.send(embed=embed, delete_after=15)

    @purge.command(description="purge before a message")
    @Check.messages()
    async def before(self, ctx, message: discord.Message, amount: PurgeAmount=None):
        """Purge messages before a given message"""
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount, before=message)
        embed = Embed(self.bot).embed(title=f"Purged {len(deleted)} messages before [message]{message.jump_url}")
        await ctx.send(embed=embed, delete_after=15)

    @commands.group(invoke_without_command=True, description="command group for slowmode")
    async def slowmode(self, ctx):
        pass
    
    @slowmode.command(description="enable slowmode in a channel")
    @Check.channels()
    async def on(self, ctx, time: TimeConverter):
        """Enable slowmode in a channel"""
        await ctx.channel.edit(slowmode_delay=time[1])
        embed = Embed(self.bot).embed()
        if time[1] == 0:
            embed.title = f"Slowmode disabled in {ctx.channel.name}"
        else:
            embed.title = f"Slowmode enabled in {ctx.channel.name} for {time[0][0]} {time[0][1]}"
        await ctx.send(embed=embed, delete_after=15)

    @slowmode.command(description="disable slowmode in a channel")
    @Check.channels()
    async def off(self, ctx: commands.Context):
        """Disable slowmode in a channel"""
        embed = Embed(self.bot).embed()
        if ctx.channel.slowmode_delay <= 0:
            embed.title = f"Slowmode is not enabled in {ctx.channel.name}"
            return await ctx.send(embed=embed, delete_after=15)
        await ctx.channel.edit(slowmode_delay=None)
        embed.title=f"Slowmode disabled in {ctx.channel.name}"
        await ctx.send(embed=embed, delete_after=15)

    @commands.command(description="Mute a member")
    @Check.moderate()
    @Check.modmute()
    async def mute(self, ctx, member: discord.Member, *, reason: ModReason=None):
        mute_id = await GuildConfigDB(self.bot.db).get_conf(ctx.guild.id, "mute")
        if not mute_id:
            return await ctx.send(embed=discord.Embed(description=f"Couldn't find a valid muted role. Please assign one using `{ctx.prefix}config mute`", colour=self.bot.red), delete_after=15)
        try:
            role = ctx.guild.get_role(int(mute_id))
        except discord.NotFound:
            return await ctx.send(embed=discord.Embed(description=f"Couldn't find a valid muted role. Please assign one using `{ctx.prefix}config mute`", colour=self.bot.red), delete_after=15)
        if role in member.roles:
            return await ctx.send(embed=discord.Embed(description=f"{member.mention} is already muted!", colour=self.bot.red), delete_after=15)
        await member.add_roles(role, reason=reason)
        await ctx.send(embed=discord.Embed(description=f"Successfully muted {member.mention}!", colour=self.bot.red))
        await self.cdb.add_case("mute", ctx.guild.id, member.id, ctx.author.id, reason, None)

    @commands.command(description="Unmutes a member")
    @Check.moderate()
    @Check.modunmute()
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        reason = "Unspecified" if reason is None else reason
        mute_id = await GuildConfigDB(self.bot.db).get_conf(ctx.guild.id, "mute")
        if not mute_id:
            return await ctx.send(embed=discord.Embed(description=f"Couldn't find a valid muted role. Please assign one using `{ctx.prefix}config mute`", colour=self.bot.red))
        try:
            role = ctx.guild.get_role(int(mute_id))
        except discord.NotFound:
            return await ctx.send(embed=discord.Embed(description=f"Couldn't find a valid muted role. Please assign one using `{ctx.prefix}config mute`", colour=self.bot.red))
        if role in member.roles:
            await member.remove_roles(role, reason=reason)
        else:
            return await ctx.send(embed=discord.Embed(description=f"{member.mention} does not have the {role.mention} role!", colour=self.bot.red))
        await ctx.send(embed=discord.Embed(description=f"Successfully unmuted {member.mention}!", colour=self.bot.red))
        await self.cdb.add_case("unmute", ctx.guild.id, member.id, ctx.author.id, reason, None)

    @commands.command(description="Temporarily mutes a member")
    @Check.moderate()
    @Check.modmute()
    async def tempmute(self, ctx, member: discord.Member, duration: MuteTime, reason: ModReason=None):
        mute_id = await GuildConfigDB(self.bot.db).get_conf(ctx.guild.id, "mute")
        if not mute_id:
            return await ctx.send(embed=discord.Embed(description=f"Couldn't find a valid muted role. Please assign one using `{ctx.prefix}config mute`", colour=self.bot.red), delete_after=15)
        try:
            role = ctx.guild.get_role(int(mute_id))
        except discord.NotFound:
            return await ctx.send(embed=discord.Embed(description=f"Couldn't find a valid muted role. Please assign one using `{ctx.prefix}config mute`", colour=self.bot.red), delete_after=15)
        if role not in member.roles:
            await member.add_roles(role, reason=reason)
        else:
            return await ctx.send(embed=discord.Embed(description=f"{member.mention} does not have the {role.mention} role!", colour=self.bot.red), delete_after=15)
        await ctx.send(embed=discord.Embed(description=f"Successfully muted {member.mention} for {duration[0][0]} {duration[0][1]}!", colour=self.bot.red))
        await self.cdb.add_case("tempmute", ctx.guild.id, member.id, ctx.author.id, reason, str(duration[1]))

    @commands.command()
    @Check.moderate()
    async def timeout(self, ctx, member: discord.Member, duration, *, reason=None):
        if not member.timed_out:
            reason = "Unspecified" if reason is None else reason
            time = Time.handler(duration)
            expirationDate = Time.convert_for_command(time)
            await member.edit(timeout_until=expirationDate)
            await ctx.send(embed=discord.Embed(description=f"{member.mention} has been timed out until {Time.parsedate(expirationDate)}.", colour=self.bot.red))
            return await self.cdb.add_case("timeout", ctx.guild.id, member.id, ctx.author.id, reason, str(expirationDate))
        await ctx.send(embed=discord.Embed(description=f"{member.mention} is already timed out.", colour=self.bot.red), delete_after=15)

    @commands.command()
    @Check.moderate()
    async def untimeout(self, ctx, member:discord.Member, reason=None):
        reason = "Unspecfied" if not reason else reason
        if member.timed_out:
            await member.edit(timeout_until=None)
            return await ctx.send(embed=discord.Embed(description=f"{member.mention} is no longer timed out.", colour=self.bot.red))
        await ctx.send(embed=discord.Embed(description=f"{member.mention} is not timed out.", colour=self.bot.red), delete_after=15)
        await self.cdb.add_case("untimeout", ctx.guild.id, member.id, ctx.author.id, reason, None)
        
    @commands.command()
    async def modstats(self, ctx, member:discord.Member=None):
        member = ctx.author if not member else member
        x = await self.cdb.get_cases_by_moderator(member.id)
        if len(x) == 0:
            return await ctx.send(embed=discord.Embed(description=f"{member.mention} has no mod stats to display!", colour=self.bot.red))
        embeds =[]
        formatted_records = self.get_chunks(5, x)
        record_num = 0
        for records in formatted_records:
            embed = discord.Embed(colour=self.bot.red).set_author(icon_url=member.avatar.url, name=f"{member.name}'s Mod Stats")
            for record in records:
                record_num +=1
                last_updated = "" if not record[7] else f"\nLast updated: {kimetsu.Time.parsedate((datetime.fromisoformat(record[7])))}"
                value = f"Case ID: {record[0]}\n" \
                        f"Case Type: {record[1].capitalize()}\n" \
                        f"Reason: {record[5]}\n" \
                        f"Punished at: {kimetsu.Time.parsedate((datetime.fromisoformat(record[6])))}{last_updated}"
                embed.add_field(name=f"Record: #{record_num}", value=value, inline=False)
                embed.set_footer(text=f"Total Records: {len(x)}")
            embeds.append(embed)
        if len(embeds) > 1:
            view = Paginator(ctx=ctx, pages=embeds)
        else:
            view = None
        await ctx.send(embed=embeds[0], view=view)
        
    @commands.command()
    @Check.messages()
    async def cases(self, ctx, member: discord.Member=None):
        member = ctx.author if not member else member
        x = await self.cdb.get_cases_for_member(member.guild.id, member.id)
        if len(x) == 0:
            return await ctx.send(embed=discord.Embed(description=f"{member.mention} has no cases to display!", colour=self.bot.red))
        embeds =[]
        formatted_cases = self.get_chunks(5, x)
        case_num = 0
        for cases in formatted_cases:
            embed = discord.Embed(colour=self.bot.red).set_author(icon_url=member.avatar.url, name=f"{member.name}'s Cases")
            for case in cases:
                case_num +=1
                last_updated = "" if not case[7] else f"\nLast updated: {kimetsu.Time.parsedate((datetime.fromisoformat(case[7])))}"
                value = f"Case ID: {case[0]}\n" \
                        f"Case Type: {case[1].capitalize()}\n" \
                        f"Reason: {case[5]}\n" \
                        f"Punished at: {kimetsu.Time.parsedate((datetime.fromisoformat(case[6])))}{last_updated}"
                embed.add_field(name=f"Record: #{case_num}", value=value, inline=False)
                embed.set_footer(text=f"Total Records: {len(x)}")
            embeds.append(embed)
        if len(embeds) > 1:
            view = Paginator(ctx=ctx, pages=embeds)
        else:
            view = None
        await ctx.send(embed=embeds[0], view=view)
        
    @commands.group(invoke_without_command=True)
    async def case(self, ctx):
        return
    
    @case.command(aliases=['update'])
    @Check.messages()
    async def edit(self, ctx, case_number: int, *, reason):
        x = await self.cdb.get_case(case_number)
        if len(x) == 0:
            return await ctx.send(embed=discord.Embed(description=f"Case #{case_number} does not exist.", colour=self.bot.red))
        member = self.bot.get_user(x[3])
        await self.cdb.update_case(case_number, reason)
        await ctx.send(embed=discord.Embed(title=f"Successfully updated case #{case_number}.", colour=self.bot.red).add_field(name="Old Reason:", value=x[5]).add_field(name="Updated Reason:", value=reason).set_author(icon_url=member.display_avatar.url, name=f"Offender: {member}").set_footer(icon_url=ctx.author.display_avatar.url, text=f"Edited by: {ctx.author}"))
        
    @case.command(aliases=['delete', 'del', 'rem', 'rm'])
    @Check.messages()
    async def remove(self, ctx, case_number: int):
        x = await self.cdb.get_case(case_number)
        if len(x) == 0:
            return await ctx.send(embed=discord.Embed(description=f"Case #{case_number} does not exist.", colour=self.bot.red))
        await self.cdb.remove_case(case_number)
        member = self.bot.get_user(x[3])
        embed=discord.Embed(title=f"Successfully deleted case #{case_number}", colour=self.bot.red).add_field(name="Case Type:", value=x[1].capitalize()).add_field(name="Issued By:", value=self.bot.get_user(x[4])).add_field(name="Issued at:", value=Time.parsedate(datetime.fromisoformat(x[6])))
        if x[5]:
            embed.add_field(name="Reason:", value=x[5])
        if x[7]:
            embed.add_field(name="Last Updated:", value=Time.parsedate(datetime.fromisoformat(x[7])))
        if x[8]:
            embed.add_field(name="Expires:", value=Time.parsedate(datetime.fromisoformat(x[8])))
        embed.set_author(icon_url=member.display_avatar.url, name=f"Offender: {member}")
        embed.set_footer(icon_url=ctx.author.display_avatar.url, text=f"Deleted by: {ctx.author}")
        await ctx.send(embed=embed)
        
    @case.command(aliases=['show', 'info'])
    @Check.messages()
    async def display(self, ctx, case_number: int=None):
        if not case_number:
            return await ctx.send(embed=discord.Embed(description="Please provide a case id to display", colour=self.bot.red))
        x = await self.cdb.get_case(case_number)
        if len(x) == 0:
            return await ctx.send(embed=discord.Embed(description=f"Case #{case_number} does not exist.", colour=self.bot.red))
        member = self.bot.get_user(x[3])
        embed=discord.Embed(colour=self.bot.red).add_field(name="Case Type:", value=x[1].capitalize()).add_field(name="Issued By:", value=self.bot.get_user(x[4])).add_field(name="Issued at:", value=Time.parsedate(datetime.fromisoformat(x[6])))
        if x[5]:
            embed.add_field(name="Reason:", value=x[5])
        if x[7]:
            embed.add_field(name="Last Updated:", value=Time.parsedate(datetime.fromisoformat(x[7])))
        if x[8]:
            embed.add_field(name="Expires:", value=Time.parsedate(datetime.fromisoformat(x[8])))
        embed.set_author(icon_url=member.display_avatar.url, name=f"Offender: {member}")
        embed.set_footer(icon_url=ctx.guild.icon.url, text=f"Case ID: #{case_number}")
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Moderation(bot))
