import discord
from discord.ext import commands
from kimetsu import embed
Embed = embed.Embed.embed

from database.prefix import PrefixDB
from database.suggestions import SuggestDB
from database.config import GuildConfigDB
from tools.components import (
    CategoriesDropdownView, 
    ChannelsDropdownView,
    ConfirmDenyView,
    SuggestConfEditMainView,
    SuggsetConfDisableView)

class ConfigCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['settings', 'conf'], invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def config(self, ctx):
        if ctx.guild.id == 912148314223415316:
            embed = discord.Embed(title="Config Panel", description="✅ = Completed, ❎ = In progress, ❌ = Not started", colour=self.bot.red)
            embed.add_field(name="Bot Settings ❎", value=f"`{ctx.prefix}config bot`")
            embed.add_field(name="Moderation Roles ❌", value=f"`{ctx.prefix}config modroles`")
            embed.add_field(name="Music DJ ❌", value=f"`{ctx.prefix}config dj`")
            embed.add_field(name="Leveling Settings ❌", value=f"`{ctx.prefix}config levels`")
            embed.add_field(name="Economy Settings ❌", value=f"`{ctx.prefix}config eco`")
            embed.set_footer(text=f"Having trouble? Join the support server using {ctx.prefix}support!")
            await ctx.send(embed=embed)

    @config.command()
    @commands.has_permissions(manage_guild=True)
    async def bot(self, ctx):
        if ctx.guild.id == 912148314223415316:
            embed = discord.Embed(title="Config Panel: Bot", colour=self.bot.red)
            embed.add_field(name="Change Prefix ✅", value=f"`{ctx.prefix}prefix <new_prefix>`")
            embed.add_field(name="Change Bot Nickname ✅", value=f"`{ctx.prefix}botnick <new_nick>`")
            embed.add_field(name="Edit Bot Responses ❌", value=f"`{ctx.prefix}config responses`")
            embed.set_footer(text=f"Having trouble? Join the support server using {ctx.prefix}support!")
            await ctx.send(embed=embed)

    @config.command(aliases=['modrole'])
    @commands.has_permissions(manage_guild=True)
    async def modroles(self, ctx):
        if ctx.guild.id == 912148314223415316:
            embed = discord.Embed(title="Config Panel: Moderation Roles", description="**NOTE:** Moderation Roles provide full access to **ALL** moderation commands as well as full **IMMUNITY** to them.", colour=self.bot.red)
            embed.add_field(name="Show Mod Roles ❌", value=f"`{ctx.prefix}modrole list`")
            embed.add_field(name="Add Mod Role ❌", value=f"`{ctx.prefix}modrole add <role>`")
            embed.add_field(name="Remove Mod Role ❌", value=f"`{ctx.prefix}modrole remove <role>`")
            embed.set_footer(text=f"Having trouble? Join the support server using {ctx.prefix}support!")
            await ctx.send(embed=embed)

    @config.command(aliases=['music'])
    @commands.has_permissions(manage_guild=True)
    async def dj(self, ctx):
        if ctx.guild.id == 912148314223415316:
            embed = discord.Embed(title="Config Panel: Music DJ", colour=self.bot.red)
            embed.add_field(name="Show DJ Roles ❌", value=f"`{ctx.prefix}dj list`")
            embed.add_field(name="Add DJ Role ❌", value=f"`{ctx.prefix}dj add <role>`")
            embed.add_field(name="Remove DJ Role ❌", value=f"`{ctx.prefix}dj remove <role>`", inline=False)
            embed.set_footer(text=f"Having trouble? Join the support server using {ctx.prefix}support!")
            await ctx.send(embed=embed)

    @config.command(aliases=['levelling', 'level'])
    @commands.has_permissions(manage_guild=True)
    async def levels(self, ctx):
        if ctx.guild.id == 912148314223415316:
            embed = discord.Embed(title="Config Panel: Levelling", colour=self.bot.red)
            embed.add_field(name="Blacklist role/member ❌", value=f"`{ctx.prefix}xp blacklist <role/member>`")
            embed.add_field(name="Add DJ Role/Member ❌", value=f"`{ctx.prefix}dj add <role/member>`")
            embed.add_field(name="Remove DJ Role/Member ❌", value=f"`{ctx.prefix}dj remove <role/member>`", inline=False)
            embed.set_footer(text=f"Having trouble? Join the support server using {ctx.prefix}support!")
            await ctx.send(embed=embed)

    @config.command(aliases=['currency', 'eco'])
    @commands.has_permissions(manage_guild=True)
    async def economy(self, ctx):
        if ctx.guild.id == 912148314223415316:
            embed = discord.Embed(title="Config Panel: Economy", colour=self.bot.red)
            embed.add_field(name="Blacklist role/member ❌", value=f"`{ctx.prefix}xp blacklist <role/member>`")
            embed.add_field(name="Add DJ Role/Member ❌", value=f"`{ctx.prefix}dj add <role/member>`")
            embed.add_field(name="Remove DJ Role/Member ❌", value=f"`{ctx.prefix}dj remove <role/member>`", inline=False)
            embed.set_footer(text=f"Having trouble? Join the support server using {ctx.prefix}support!")
            await ctx.send(embed=embed)

    @config.command(description="change the bot's prefix", aliases=["config prefix"])
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, new_prefix=None):
        """Change the bot's prefix"""
        if new_prefix is None:
            embed = Embed(
                title=f"The prefix for `{ctx.guild.name}` is `{ctx.prefix}`", 
                timestamp=True
            )
            return await ctx.message.reply(embed=embed)
        
        con = PrefixDB(self.bot.db)
        await con.update(ctx.guild.id, new_prefix)
        
        embed = Embed(
            title=f"Prefix for `{ctx.guild.name}` set to `{new_prefix}`",
            timestamp=True
        )
        
        return await ctx.message.reply(embed=embed)

    @config.command()
    @commands.has_permissions(manage_nicknames=True)
    async def botnick(self, ctx, *, nickname: str=None):
        if nickname is None:
            return await ctx.send(embed=discord.Embed(description=f"My nickname is **{ctx.guild.me.display_name}**!", colour=self.bot.red))
        oldnick = ctx.guild.me.display_name
        if nickname.lower() == "reset":
            nickname = self.bot.user.name
        await ctx.guild.me.edit(nick=nickname)
        await ctx.send(embed=discord.Embed(description=f"Successfully changed my nickname from **{oldnick}** -> **{nickname}**!", colour=discord.Colour.green()))

    @config.command(aliases=['suggest', 'suggestion'])
    @commands.has_permissions(manage_guild=True)
    async def suggestions(self, ctx):
        guildconf = await SuggestDB(self.bot.db).getconf(ctx.guild.id)
        if guildconf is None:
            """   SELECT CATEGORY OF THE SUGGESTIONS CHANNEL   """
            view = CategoriesDropdownView(ctx)
            embed = discord.Embed(description="Please select the category in which your desired suggestions channel is in below.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon, name="Suggestions Setup")
            msg = await ctx.send(embed=embed, view=view)
            await view.wait()
            cat_id = view.values[0]
            embed.description += f"\n\n**[EXPIRED] - Category Chosen:** `{ctx.guild.get_channel(int(cat_id)).name}`"
            await msg.edit(embed=embed, view=None)

            """   SELECT CHANNEL WITHIN CHOSEN CATEGORY   """
            view = ChannelsDropdownView(ctx.guild.get_channel(int(cat_id)), ctx)
            embed = discord.Embed(description="Please select the channel that you would like suggestions to be sent to below.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Setup")
            msg = await ctx.send(embed=embed, view=view)
            await view.wait()
            channel_id = view.values[0]
            embed.description += f"\n\n**[EXPIRED] - Channel Chosen:** {ctx.guild.get_channel(int(channel_id)).mention}"
            await msg.edit(embed=embed, view=None)

            """   SAFEMODE ENABLE/DISABLE   """
            view = ConfirmDenyView(ctx)
            embed = discord.Embed(description="**Would you like to enable safemode?**\n\n> Safemode means that a suggestion will have to be allowed by a higher-up before being sent into your suggestions channel. Please select a button below to either enable/disable safemode.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Setup")
            msg = await ctx.send(embed=embed, view=view)
            await view.wait()
            safemodebool = view.value
            embed.description += f"\n\n**[EXPIRED] - Safemode is:** `{'Enabled' if safemodebool is True else 'Disabled'}`"
            await msg.edit(embed=embed, view=None)

            """   ADD CONFIG TO DATABASE IF NOT SAFEMODE   """
            if not safemodebool:
                await SuggestDB(self.bot.db).setupnon(ctx.guild.id, int(channel_id))

            """   GET SAFEMODE CAT IF ENABLED """
            if safemodebool:
                view = CategoriesDropdownView(ctx)
                embed = discord.Embed(description="Please select the Category for the channel that you want suggestions to await acceptance in.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Setup")
                msg = await ctx.send(embed=embed, view=view)
                await view.wait()
                safemodecat = view.values[0]
                embed.description += f"\n\n**[EXPIRED] - Category Chosen:** `{ctx.guild.get_channel(int(safemodecat)).name}`"
                await msg.edit(embed=embed, view=None)

                """GET SAFEMODE CHANNEL IF ENABLED"""
                view = ChannelsDropdownView(ctx.guild.get_channel(int(safemodecat)), ctx)
                embed = discord.Embed(description="Select the channel that you want suggestions to await acceptance in.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Setup")
                msg = await ctx.send(embed=embed, view=view)
                await view.wait()
                safemodechannel = view.values[0]
                embed.description += f"\n\n**[EXPIRED] - Channel Chosen:** {ctx.guild.get_channel(int(safemodechannel)).mention}"

                """   ADD CONFIG TO DATABASE   """
                await SuggestDB(self.bot.db).setup(ctx.guild.id, int(channel_id), int(safemodechannel))
            
            """   CONFIRMATION MESSAGE   """
            await ctx.message.reply(embed=discord.Embed(description=f"Suggestions has been successfully setup for `{ctx.guild.name}`!\n\nIf you made a mistake or would like to make edits in future, simply run `{ctx.prefix}config suggestions` again!\n\n**NEW CONFIGURATION:**\nChannel: {ctx.guild.get_channel(int(channel_id)).mention}\nSafemode: {f'Enabled in {ctx.guild.get_channel(int(safemodechannel)).mention}' if safemodebool else 'Disabled'}", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Setup Complete"))
        elif guildconf:
            """   ASK USER WHAT THEY WOULD LIKE TO EDIT   """
            view = SuggestConfEditMainView(ctx)
            if guildconf[1] is None:
                safemode = "Disabled"
            else:
                safemode = f"<#{guildconf[1]}>"
            embed = discord.Embed(description=f"What suggestions setting would you like to edit?\n\n**Current Configuration:**\n> Suggestions Channel: <#{guildconf[0]}>\n> Safemode: {safemode}", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Config")
            msg = await ctx.send(embed=embed, view=view)
            await view.wait()
            setting_to_change = view.values[0]
            embed.description += f"\n\n**[EXPIRED] - Setting Selected:** `{setting_to_change}`"
            await msg.edit(embed=embed, view=None)
            """   IF EDIT SUGGESTIONS CHANNEL:   """
            if setting_to_change == "Suggestions Channel":
                """   GET CHANNEL CATEGORY   """
                embed = discord.Embed(description="Please select the category in which your desired suggestions channel is in below.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon, name="Suggestions Config")
                view = CategoriesDropdownView(ctx)
                msg = await ctx.send(embed=embed, view=view)
                await view.wait()
                category = view.values[0]
                embed.description += f"\n\n**[EXPIRED] - Category Selected:** `{ctx.guild.get_channel(int(category)).name}`"
                await msg.edit(embed=embed, view=None)
                """   GET CHANNEL FROM CATEGORY   """
                embed = discord.Embed(description="Please select the channel that you would like suggestions to be sent to below.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Config")
                view = ChannelsDropdownView(self.bot.get_channel(int(category)), ctx)
                msg = await ctx.send(embed=embed, view=view)
                await view.wait()
                channel = view.values[0]
                embed.description += f"\n\n**[EXPIRED] - Channel Selected:** {ctx.guild.get_channel(int(channel)).mention}"
                await msg.edit(embed=embed, view=None)
                """   UPDATE DATABASE   """
                await SuggestDB(self.bot.db).updatechannel(ctx.guild.id, int(channel))
                """   SEND CONFIRMATION MESSAGE   """
                return await ctx.message.reply(embed=discord.Embed(description=f"Suggestion channel has been modified for `{ctx.guild.name}`!\n\nIf you made a mistake or would like to make edits in future, simply run `{ctx.prefix}config suggestions` again!\n\n**NEW CONFIGURATION:**\nChannel: {ctx.guild.get_channel(int(channel)).mention}\nSafemode: {safemode}", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Config"))
            elif setting_to_change == "Safemode":
                """   GET SAFEMODE CATEGORY   """
                embed = discord.Embed(description="Please select the category in which your desired safemode channel is in below.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon, name="Suggestions Config")
                view = CategoriesDropdownView(ctx, guildconf[1])
                msg = await ctx.send(embed=embed, view=view)
                await view.wait()
                category = view.values[0]
                if category == "Disable":
                    await SuggestDB(self.bot.db).updatesafemode(ctx.guild.id, None)
                    embed.description += f"\n\n**[EXPIRED] -** Safemode has been `disabled`"
                    return await msg.edit(embed=embed, view=None)
                embed.description += f"\n\n**[EXPIRED] - Category Selected:** `{ctx.guild.get_channel(int(category)).name}`"
                await msg.edit(embed=embed, view=None)
                """   GET SAFEMODE CHANNEL   """
                embed = discord.Embed(description="Please select the channel that you would like safemode suggestions to be sent to below.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Config")
                view = ChannelsDropdownView(self.bot.get_channel(int(category)), ctx)
                msg = await ctx.send(embed=embed, view=view)
                await view.wait()
                channel = view.values[0]
                embed.description += f"\n\n**[EXPIRED] - Channel Selected:** {ctx.guild.get_channel(int(channel)).mention}"
                await msg.edit(embed=embed, view=None)
                """   UPDATE DATABASE   """
                await SuggestDB(self.bot.db).updatesafemode(ctx.guild.id, int(channel))
                """   SEND CONFIRMATION MESSAGE   """
                return await ctx.message.reply(embed=discord.Embed(description=f"Suggestion channel has been modified for `{ctx.guild.name}`!\n\nIf you made a mistake or would like to make edits in future, simply run `{ctx.prefix}config suggestions` again!\n\n**NEW CONFIGURATION:**\nChannel: {ctx.guild.get_channel(int(guildconf[0])).mention}\nSafemode: <#{channel}>", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Config"))
            elif setting_to_change == "Disable":
                view = SuggsetConfDisableView(ctx)
                embed = discord.Embed(description="Are you sure you want to disable the suggestion feature?", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Config")
                msg = await ctx.send(embed=embed, view=view)
                await view.wait()
                disabled = view.value
                if disabled:
                    await SuggestDB(self.bot.db).shutdown(ctx.guild.id)
                    embed.description += f"\n\n**[EXPIRED] - Option Selected:** `Disable Feature`"
                    await msg.edit(embed=embed, view=None)
                elif not disabled:
                    embed.description += f"\n\n**[EXPIRED] - Option Selected:** `Don't Disable Feature`"
                    await msg.edit(embed=embed, view=None)

    @config.command(aliases=['mute'])
    @commands.has_permissions(manage_guild=True)
    async def addmute(self, ctx, muterole: discord.Role):
        await GuildConfigDB(self.bot.db).add_conf(ctx.guild.id, "mute", muterole.id)
        await ctx.send(embed=discord.Embed(description=f"Successfully assigned mute role to {muterole.mention}!", colour=self.bot.red))

def setup(bot):
    bot.add_cog(ConfigCMD(bot))