import discord
from discord.ext import commands
from .error_messages import *
from database.config import GuildConfigDB

class Check:
    async def getmodules(ctx):
        modules = await GuildConfigDB(ctx.bot.db).get_module(ctx.guild.id)
        return modules

    def module(module: str):
        async def predicate(ctx: commands.Context):
            modules = await Check.getmodules(ctx)
            try:
                modules[module]
            except KeyError:
                raise DevError
            if modules[module]:
                return True
            else:
                raise ModuleDisabled("ban")
        return commands.check(predicate)
    
    def owner():
        async def predicate(ctx: commands.Context):
            return await ctx.bot.is_owner(ctx.author)
        return commands.check(predicate)

    def admin():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.administrator or not ctx.guild.me.guild_permissions.administrator:
                raise BasicFailure("You are missing the `ADMINISTRATOR` permission to run this command.")
            return ctx.author.guild_permissions.administrator
        return commands.check(predicate)

    def ban():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.ban_members or not ctx.guild.me.guild_permissions.ban_members:
                raise BasicFailure("You are missing the `BAN MEMBERS` permission to run this command.")
            return ctx.author.guild_permissions.ban_members
        return commands.check(predicate)

    def deaf():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.deafen_members or not ctx.guild.me.guild_permissions.deafen_members:
                raise BasicFailure("You are missing the `DEAFEN MEMBERS` permission to run this command.")
            return ctx.author.guild_permissions.deafen_members
        return commands.check(predicate)

    def kick():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.kick_members or not ctx.guild.me.guild_permissions.kick_members:
                raise BasicFailure("You are missing the `KICK MEMBERS` permission to run this command.")
            return ctx.author.guild_permissions.kick_members
        return commands.check(predicate)

    def channels():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.manage_channels or not ctx.guild.me.guild_permissions.manage_channels:
                raise BasicFailure("You are missing the `MANAGE CHANNELS` permission to run this command.")
            return ctx.author.guild_permissions.manage_channels
        return commands.check(predicate)

    def emojis_and_stickers():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.manage_emojis_and_stickers or not ctx.guild.me.guild_permissions.manage_emojis_and_stickers:
                raise BasicFailure("You are missing the `MANAGE EMOJIS AND STICKERS` permission to run this command.")
            return ctx.author.guild_permissions.manage_emojis_and_stickers
        return commands.check(predicate)

    def emojis():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.manage_emojis or not ctx.guild.me.guild_permissions.manage_emojis:
                raise BasicFailure("You are missing the `MANAGE EMOJIS` permission to run this command.")
            return ctx.author.guild_permissions.manage_emojis
        return commands.check(predicate)

    def events():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.manage_events or not ctx.guild.me.guild_permissions.manage_events:
                raise BasicFailure("You are missing the `MANAGE EVENTS` permission to run this command.")
            return ctx.author.guild_permissions.manage_events
        return commands.check(predicate)

    def guild():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.manage_guild or not ctx.guild.me.guild_permissions.manage_guild:
                raise BasicFailure("You are missing the `MANAGE GUILD` permission to run this command.")
            return ctx.author.guild_permissions.manage_guild
        return commands.check(predicate)

    def messages():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.manage_messages or not ctx.guild.me.guild_permissions.manage_messages:
                raise BasicFailure("You are missing the `MANAGE MESSAGES` permission to run this command.")
            return ctx.author.guild_permissions.manage_messages
        return commands.check(predicate)

    def nicknames():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.manage_nicknames or not ctx.guild.me.guild_permissions.manage_nicknames:
                raise BasicFailure("You are missing the `MANAGE NICKNAMES` permission to run this command.")
            return ctx.author.guild_permissions.manage_nicknames
        return commands.check(predicate)

    def permissions():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.manage_permissions or not ctx.guild.me.guild_permissions.manage_permissions:
                raise BasicFailure("You are missing the `MANAGE PERMISSIONS` permission to run this command.")
            return ctx.author.guild_permissions.manage_permissions
        return commands.check(predicate)

    def roles():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.manage_roles or not ctx.guild.me.guild_permissions.manage_roles:
                raise BasicFailure("You are missing the `MANAGE ROLES` permission to run this command.")
            return ctx.author.guild_permissions.manage_roles
        return commands.check(predicate)

    def moderate():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.moderate_members or not ctx.guild.me.guild_permissions.moderate_members:
                raise BasicFailure("You are missing the `MODERATE MEMBERS` permission to run this command.")
            return ctx.author.guild_permissions.moderate_members
        return commands.check(predicate)

    def move():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.move_members or not ctx.guild.me.guild_permissions.move_members:
                raise BasicFailure("You are missing the `MOVE MEMBERS` permission to run this command.")
            return ctx.author.guild_permissions.move_members
        return commands.check(predicate)

    def mute():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.mute_members or not ctx.guild.me.guild_permissions.mute_members:
                raise BasicFailure("You are missing the `MUTE MEMBERS` permission to run this command.")
            return ctx.author.guild_permissions.mute_members
        return commands.check(predicate)

    def audit():
        async def predicate(ctx: commands.Context):
            if not ctx.author.guild_permissions.view_audit_log or not ctx.guild.me.guild_permissions.view_audit_log:
                raise BasicFailure("You are missing the `VIEW AUDIT LOG` permission to run this command.")
            return ctx.author.guild_permissions.view_audit_log
        return commands.check(predicate)

    def moderation():
        async def predicate(ctx: commands.Context):
            for arg in ctx.args:
                if isinstance(arg, discord.Member):
                    if arg == ctx.author:
                        raise TargetAuthor(ctx)
                    elif arg.top_role > ctx.author.top_role and ctx.author is not ctx.guild.owner:
                        raise Hierarchy
            return True
        return commands.check(predicate)
    
    def modmute():
        async def predicate(ctx: commands.Context):
            for arg in ctx.args:
                if isinstance(arg, discord.Member):
                    role = ctx.guild.get_role(await GuildConfigDB(ctx.bot.db).get_conf(ctx.guild.id, "mute"))
                    if role in arg.roles:
                        raise AlreadyMuted(arg)
                    return True
        return commands.check(predicate)
    
    def modunmute():
        async def predicate(ctx: commands.Context):
            for arg in ctx.args:
                if isinstance(arg, discord.Member):
                    role = ctx.guild.get_role(await GuildConfigDB(ctx.bot.db).get_conf(ctx.guild.id, "mute"))
                    if role not in arg.roles:
                        raise NotMuted(arg)
                    return True
        return commands.check(predicate)