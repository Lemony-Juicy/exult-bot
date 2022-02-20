import discord
from discord.ext import commands

class BasicFailure(commands.CheckFailure):
    def __init__(self, msg):
        super().__init__(msg)
        
class ModuleDisabled(commands.CheckFailure):
    def __init__(self, module):
        super().__init__(f"The {module} module is currently disabled. Please enable it on our [dashboard](https://bot.exult.games)!")
        
class DevError(commands.CheckFailure):
    def __init__(self):
        super().__init__("Apologies, there was an error on our end. Please report this on our [GitHub](https://github.com/andeh-py/exult-bot/issues)")

class NotPremium(commands.CheckFailure):
    def __init__(self, ctx):
        super().__init__(f"This feature is for premium users only! Looking to be a premium user? Do `{ctx.prefix}premium`!")

class TargetAuthor(commands.CheckFailure):
    def __init__(self, ctx: commands.Context):
        super().__init__(f"You cannot {ctx.command.name} yourself.")

class Hierarchy(commands.CheckFailure):
    def __init__(self):
        super().__init__("You cannot mute someone with a higher role than you.")

class NotBotOwner(commands.CheckFailure):
    def __init__(self):
        super().__init__("Only the bot owner can run that command.")

class NotGuildOwner(commands.CheckFailure):
    def __init__(self, ctx):
        super().__init__(f"Only the server owner ({ctx.guild.owner}) can run that command.")

class NotServerStaff(commands.CheckFailure):
    def __init__(self, ctx):
        super().__init__(f"Only server moderators can run that command. If this is a mistake, view your settings on the [dashboard](https://bot.exult.games)")
        
class AlreadyMuted(commands.CheckFailure):
    def __init__(self, member: discord.Member):
        super().__init__(f"{member} is already muted!")
        
class NotMuted(commands.CheckFailure):
    def __init__(self, member: discord.Member):
        super().__init__(f"{member} is not muted!")

