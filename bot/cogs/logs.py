import discord
from discord.ext import commands

from typing import Literal, Union

from database.logs import LogsDB

from pprint import pformat

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = LogsDB(bot.db)
        self.andeh = bot.get_user(839248459704959058)

    events = Literal['channel_create', 'channel_delete', 'channel_update', 'guild_update', 'guild_emoji_update', 'guild_sticker_update',
                     'invite_create', 'invite_delete', 'intergration_update', 'webhook_update', 'member_join', 'member_remove',
                     'member_update', 'user_update', 'member_ban', 'member_unban', 'message_edit', 'message_delete', 'bulk_message_delete',
                     'role_create', 'role_delete', 'role_update', 'voice_update']

    def second_handler(self, num: int):
        m, s = divmod(num, 60)
        h, m = divmod(m, 60)
        hours = f"{h} hour " if h == 1 else f"{h} hours "
        minutes = f"{m} minute " if m == 1 else f"{m} minutes "
        seconds = f"{s} second " if s == 1 else f"{s} seconds "
        hours = "" if h == 0 else hours
        minutes = "" if m == 0 else minutes
        seconds = "" if s == 0 else seconds
        hms = f"{hours}{minutes}{seconds}"
        hms = "None" if hms == "" else hms
        return hms

    @commands.command()
    @commands.is_owner()
    async def addlog(self, ctx, event: events, channel: Union[discord.TextChannel, int]):
        if isinstance(channel, discord.TextChannel):
            channel_id = channel.id
        elif isinstance(channel, int):
            channel_id = channel
        await self.db.update(ctx.guild.id, event, channel_id)
        await ctx.send(embed=discord.Embed(description=f"Successfully bound `{event.replace('_', ' ').upper()}` event to <#{channel_id}>", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Logs Setup"))

    @commands.command()
    @commands.is_owner()
    async def editlog(self, ctx, event: events, channel: Union[discord.TextChannel, int]):
        if isinstance(channel, discord.TextChannel):
            channel_id = channel.id
        elif isinstance(channel, int):
            channel_id = channel
        await self.db.update(ctx.guild.id, event, channel_id)
        await ctx.send(embed=discord.Embed(description=f"Successfully bound `{event.replace('_', ' ').upper()}` event to <#{channel_id}>", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Logs Config"))

    @commands.command()
    @commands.is_owner()
    async def dellog(self, ctx, event: events):
        await self.db.remove(ctx.guild.id, event)
        await ctx.send(embed=discord.Embed(description=f"Successfully removed `{event.replace('_', ' ').upper()}`", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Logs Config"))

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        if channel.guild.id != 912148314223415316: return
        log_channel_id = await self.db.get(channel.guild.id, 'channel_delete')
        if not log_channel_id:
            return
        log_channel = self.bot.get_channel(log_channel_id)
        if str(channel.type) == 'text':
            header = "Text Channel Deleted | Log"
        elif str(channel.type) == 'voice':
            header = "Voice Channel Deleted | Log"
        elif str(channel.type) == 'news':
            header = "Announcement Channel Deleted | Log"
        elif str(channel.type) == 'stage_voice':
            header = "Stage Channel Deleted | Log"
        elif str(channel.type) == 'category':
            header = "Category Deleted | Log"
        name = channel.name
        category = channel.category
        topic = f"\n**Topic:**\n```\n{channel.topic}\n```" if str(channel.type) == 'text' and channel.topic else ""
        action = discord.AuditLogAction.channel_delete
        async for log in channel.guild.audit_logs(action=action, limit=1):
            user = log.user
        description = f"**Name:** {name}\n**Category:** {category}\n**Deleted by:** {user}{topic}"
        embed = discord.Embed(description=description, colour=self.bot.red).set_author(icon_url=channel.guild.icon.url, name=header).set_footer(icon_url=user.display_avatar.url, text=f"Deleted by {log.user}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        if channel.guild.id != 912148314223415316: return
        log_channel_id = await self.db.get(channel.guild.id, 'channel_create')
        if not log_channel_id:
            return
        log_channel = self.bot.get_channel(log_channel_id)
        if str(channel.type) == 'text':
            header = "Text Channel Created | Log"
        elif str(channel.type) == 'voice':
            header = "Voice Channel Created | Log"
        elif str(channel.type) == 'stage_voice':
            header = "Stage Channel Created | Log"
        elif str(channel.type) == 'category':
            header = "Category Created | Log"
        name = channel.name
        mention = channel.mention
        category = channel.category
        action = discord.AuditLogAction.channel_create
        async for log in channel.guild.audit_logs(action=action, limit=1):
            user = log.user
        description = f"**Name:** {name}\n**Mention:** {mention}\n**Category:** {category}"
        embed = discord.Embed(description=description, colour=discord.Colour.green()).set_author(icon_url=channel.guild.icon.url, name=header).set_footer(icon_url=user.display_avatar.url, text=f"Created by {user}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after):
        if before.guild.id != 912148314223415316: return
        log_channel_id = await self.db.get(before.guild.id, 'channel_update')
        log_channel = self.bot.get_channel(log_channel_id)
        action = discord.AuditLogAction.channel_update
        async for log in after.guild.audit_logs(limit=1, action=action):
            user = log.user
        if str(before.type) == 'text':
            if before.topic != after.topic:
                header = "Channel Topic Updated | Log"
                description = f"**Before:**```{before.topic}```**After:**```{after.topic}```"
            elif before.nsfw != after.nsfw:
                header = "Channel NSFW Updated | Log"
                description = f"**Before:** {before.nsfw}\n**After:** {after.nsfw}"
            elif before.slowmode_delay != after.slowmode_delay:
                before_delay = self.second_handler(before.slowmode_delay)
                after_delay = self.second_handler(after.slowmode_delay)
                header = "Channel Slowmode Updated | Log"
                description = f"**Before:** {before_delay}\n**After:** {after_delay}"
        elif str(before.type) == 'voice' or str(before.type) == 'stage_voice':
            header = "Voice Channel Updated | Log" if str(before.type) == 'voice' else "Stage Channel Updated | Log"
            if before.bitrate != after.bitrate:
                header = "Channel Bitrate Updated | Log"
                description = f"**Before:** {before.bitrate}bps\n**After:** {after.bitrate}bps"
            elif before.rtc_region != after.rtc_region:
                header = "Channel Region Updated | Log"
                description = f"**Before:** {before.rtc_region.capitalize()}\n**After:** {after.rtc_region.capitalize()}" 
            elif before.user_limit != after.user_limit:
                header = "Channel User Limit Updated | Log"
                description = f"**Before:** {before.user_limit} users\n**After:** {after.user_limit} users"
        #if before.overwrites != after.overwrites:
        #    header = "Channel Overwrites Updated | Log"
        #    before_changed = []
        #    after_changed = []
        #    for key in before.overwrites:
        #        before_changed.append((key, before.overwrites[key]))
        #    for key in after.overwrites:
        #        after_changed.append((key, after.overwrites[key]))
        #    for perm in after_changed:
        #        if perm not in before_changed:
        #            perm_iter = iter(perm)
        #            await self.andeh.send(f"Role/Member = {next(perm_iter)}")
        #            perm_test = discord.PermissionOverwrite.pair(next(perm_iter))
        #            await self.andeh.send(f"perm_test = {perm_test[0]}")
        #            await self.andeh.send(f"perm_test2 = {perm_test[1]}")
        if before.category != after.category:
            header = "Channel Category Updated | Log"
            description = f"**Before:** {before.category.name}\n**After:** {after.category.name}"
        elif before.name != after.name:
            header = "Channel Name Updated | Log"
            description = f"**Before:** {before.name}\n**After:** {after.name}"
        if not description:
            return
        embed = discord.Embed(description=description, colour=self.bot.red).set_author(icon_url=after.guild.icon.url, name=header).set_footer(icon_url=user.display_avatar.url, text=f"Changed by: {user}")
        await log_channel.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        if before.id not in [912148314223415316, 652899105496104960]: return
        log_channel_id = await self.db.get(before.id, 'guild_update')
        log_channel = self.bot.get_channel(log_channel_id)
        action = discord.AuditLogAction.guild_update
        async for log in after.audit_logs(limit=1, action=action):
            user = log.user
        embed = discord.Embed(colour=self.bot.red)
        if before.afk_channel != after.afk_channel:
            header = "Server AFK Channel Updated | Log"
            before_channel = "None" if not before.afk_channel else before.afk_channel.mention
            after_channel = "None" if not after.afk_channel else after.afk_channel.mention
            description=f"**Before:** {before_channel}\n**After:** {after_channel}"
        elif before.afk_timeout != after.afk_timeout: 
            header = "Server AFK Timeout Updated | Log"
            before_time = self.second_handler(before.afk_timeout)
            after_time = self.second_handler(after.afk_timeout)
            description = f"**Before:** {before_time}\n**After:** {after_time}"
        elif before.banner != after.banner: 
            header = "Server Banner Updated | Log"
            description = "Banner Disabled" if not after.banner else f"[View Banner]({after.banner.url})"
            if after.banner:
                embed.set_image(url=after.banner.url)
        elif before.description != after.description: 
            header = "Server Description Updated | Log"
            description = f"**Before:**```\n{before.description}```**After:**```\n{after.description}```"
        elif before.icon != after.icon: 
            header = "Server Icon Updated | Log"
            description = "Icon Disabled" if not after.icon else f"[View Icon]({after.icon.url})"
            if after.icon:
                embed.set_image(url=after.icon.url)
        elif before.name != after.name: 
            header = "Server Name Updated | Log"
            description = f"**Before:** {before.name}\n**After:** {after.name}"
        elif before.owner != after.owner:
            header = "Server Owner Updated | Log"
            description = f"**Before:** {before.owner}\n**After:** {after.owner}"
        if not after.icon:
            embed.set_author(name=header)
        elif after.icon:
            embed.set_author(icon_url=after.icon.url, name=header)
        embed.set_footer(icon_url=user.display_avatar.url, text=f"Changed by: {user}")
        embed.description = description
        await log_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before: discord.Emoji, after: discord.Emoji):
        return

    @commands.Cog.listener()
    async def on_guild_stickers_update(self, guild: discord.Guild, before: discord.GuildSticker, after: discord.GuildSticker):
        return

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):
        return

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite):
        return

    @commands.Cog.listener()
    async def on_guild_integrations_update(self, guild: discord.Guild):
        return

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel: discord.abc.GuildChannel):
        return

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        return

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        return

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        return

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        return

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        return

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        return

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        return

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        return

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages: list):
        return

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        return

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        return

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        return

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        return

def setup(bot):
    bot.add_cog(Logs(bot))