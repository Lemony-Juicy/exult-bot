import discord
from discord.ext import commands
import sys
import traceback
import math


def conv_n(tuple_acc):
    returning = ""
    op_list_v = []
    op_list_n = list(tuple_acc)
    for i in range(len(op_list_n)):
        op_list_v.append(op_list_n[i].__name__.replace("Converter", ""))
    for i in range(len(op_list_v)):
        if i + 3 <= len(op_list_v):
            returning += f"{op_list_v[i].lower()}, "
        elif i + 2 <= len(op_list_v):
            returning += f"{op_list_v[i].lower()} or "
        else:
            returning += f"{op_list_v[i].lower()}"
    return returning


class ErrorHandler(commands.Cog):
    """The bot error handler."""

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, "on_error"):
            return

        error = getattr(error, "original", error)
        if isinstance(error, commands.CommandNotFound):
            if len(ctx.message.content[2:]) < 4:
                return
            possiblecmds = ""
            for cmd in self.bot.walk_commands():
                if ctx.message.content[2:] in cmd.qualified_name:
                    possiblecmds += f"{cmd.qualified_name}\n"
            if len(possiblecmds) < 1:
                return
            await ctx.send(embed=discord.Embed(title="Uncrecognised command!", description=f"Sorry, I didn't recognise that command, perhaps you meant any of the following?\n\n{possiblecmds}", colour=self.bot.red))

        elif isinstance(error, commands.BadUnionArgument):
            embed = discord.Embed(
                colour=self.bot.red,
                title="Bad argument",
                description=f"You did not provide a valid {conv_n(error.converters)}, please go check `{ctx.clean_prefix}help {ctx.command.name}`.",
            )
            await ctx.send(embed=embed, delete_after=15)

        elif isinstance(error, commands.UserNotFound):
            embed = discord.Embed(
                colour=self.bot.red,
                title="User not found",
                description=f"You did not provide a valid user, please go check `{ctx.clean_prefix}help {ctx.command.name}`.",
            )
            await ctx.send(embed=embed, delete_after=15)

        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                colour=self.bot.red,
                title="Member not found",
                description=f"You did not provide a valid member, Please go check `{ctx.clean_prefix}help {ctx.command.name}`.",
            )
            await ctx.send(embed=embed, delete_after=15)

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
            if len(missing) > 2:
                fmt = f"{'**, **'.join(missing[:-1])}, and { missing[-1]}"
            else:
                fmt = " and ".join(missing)
                _message = f"I need the **{fmt}** permission(s) to run this command."
                embed = discord.Embed(
                    colour=self.bot.red,
                    title="Bot missing permissions",
                    description=_message,
                )
                await ctx.send(embed=embed)

        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(
                colour=self.bot.red,
                title="Command disabled",
                description=f"This command has been temporaly disabled, it is probably under maintenance. For more informations join the [support server](https://discord.gg/Hg8kU9pmx9) !",
            )
            await ctx.send(embed=embed, delete_after=15)
        elif isinstance(error, commands.MaxConcurrencyReached):
            _message = f"This command can only be used **{error.number}** time simultaneously, please retry later."
            embed = discord.Embed(
                colour=self.bot.red,
                title="Maximum concurrency reached",
                description=_message,
            )
            await ctx.send(embed=embed, delete_after=15)

        elif isinstance(error, commands.CommandOnCooldown):
            _message = "This command is on cooldown, please retry in {}.".format(
                my_tools.human_readable(math.ceil(error.retry_after))
            )
            embed = discord.Embed(
                colour=self.bot.red, title="Command on cooldown", description=_message
            )
            await ctx.send(embed=embed, delete_after=15)

        elif isinstance(error, commands.MissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
            if len(missing) > 2:
                fmt = f"{'**, **'.join(missing[:-1])}, and {missing[-1]}"
            else:
                fmt = " and ".join(missing)
                _message = f"You need the **{fmt}** permission(s) to use this command."
                embed = discord.Embed(
                    colour=self.bot.red,
                    title="Missing permissions",
                    description=_message,
                )
                await ctx.send(embed=embed, delete_after=15)

        elif isinstance(error, commands.MissingRole):
            missing = error.missing_role
            _message = f"You need the **{missing}** role to use this command."
            embed = discord.Embed(title="Missing role", description=_message)
            await ctx.send(embed=embed, delete_after=15)

        elif isinstance(error, discord.Forbidden):
            _message = "Sorry I cannot run this command."
            embed = discord.Embed(
                colour=self.bot.red, title="Forbidden", description=_message
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.NSFWChannelRequired):
            _message = "Sorry, I cannot display NSFW content in this channel."
            embed = discord.Embed(
                colour=self.bot.red,
                stitle="NSFW channel required",
                description=_message,
            )
            await ctx.send(embed=embed, delete_after=15)
        elif isinstance(error, commands.BadArgument):
            _message = f"You provided at least one wrong argument. Please go check `{ctx.clean_prefix}help {ctx.command}`"
            embed = discord.Embed(
                colour=self.bot.red, title="Bad argument", description=_message
            )
            await ctx.send(embed=embed, delete_after=15)

        elif isinstance(error, commands.UserInputError):
            _message = f"You made an error in your commmand. Please go check `{ctx.clean_prefix}help {ctx.command}`"
            embed = discord.Embed(
                colour=self.bot.red, title="Input error", description=_message
            )
            await ctx.send(embed=embed, delete_after=15)

        elif isinstance(error, commands.NoPrivateMessage):
            _message = "This command cannot be used in direct messages. Please retry in a guild."
            embed = discord.Embed(
                colour=self.bot.red, title="No private message", description=_message
            )
            try:
                await ctx.send(embed=embed, delete_after=15)
            except discord.Forbidden:
                pass
            return
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                colour=self.bot.red,
                title="Owner-only",
                description=f"Sorry **{ctx.author}**, but this commmand is an owner-only command and you don't look like {self.bot.get_user(self.bot.owner_ids[0]).name}.",
            )
            await ctx.send(embed=embed, delete_after=15)
        elif isinstance(error, commands.CheckFailure):
            return
        else:

            try:
                embed = discord.Embed(
                    colour=self.bot.red,
                    title="❌ Error",
                    description="Sorry, an error has occured, it has been reported to my developer.",
                )
                embed.add_field(
                    name="Traceback :",
                    value=f"```py\n{type(error).__name__} : {error}```",
                )
                await ctx.send(embed=embed)
                trcb = traceback.format_exception(
                    type(error), error, error.__traceback__, limit=None, chain=True
                )
                traceback_text = "".join(trcb)[0:2000]
                channel = self.bot.get_channel(830964323412607016)
                embed_rep = discord.Embed(
                    colour=self.bot.red,
                    title="Error",
                    description="```py\nIgnoring exception in command {}:\n{}```".format(
                        ctx.command, traceback_text
                    ),
                )
                embed_rep.set_footer(
                    text=f"Requested by: {ctx.author} | ID : {ctx.author.id} | Command: {ctx.command}",
                    icon_url=ctx.author.avatar.url,
                )
                await channel.send(embed=embed_rep)
            except:
                pass

            # ignore all other exception types, but print them to stderr
            print(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
