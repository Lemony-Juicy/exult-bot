import discord
from discord import app_commands, Interaction

import datetime

from utils import *
from database import *
    
class ModLogging:
    def __init__(self, *, action:str=None, interaction:Interaction=None, member:discord.User=None, reason:str=None, expiration_date:str=None):
        self.action = action
        self.db = CasesDB(Database())
        self.interaction = interaction
        self.member = member
        self.reason = reason
        self.expire = expiration_date
        
    async def handle_case(self, return_log_channel:bool):
        inter = self.interaction
        member = self.member
        reason = self.reason
        expire = self.expire
        case = await self.db.add_case(self.action, inter.guild.id, member.id, inter.user.id, reason, expire, True)
        logembed = embed_builder(author=[inter.user.display_avatar.url, f"Case {case} | {self.action.capitalize()}"],
                                 thumbnail=member.display_avatar.url,
                                 fields=[["User:", member.mention, False], ["Moderator:", inter.user.mention, False],
                                         ["Reason:", reason, False]])
        if return_log_channel:
            return [logembed, 934482344155435028]
        return logembed
    
    async def get_cases_by_moderator(self, moderator: discord.User):
        CASES = await self.db.get_cases_by_moderator(moderator.id)
        if len(CASES) == 0:
            embed = embed_builder(description=f"{moderator.mention} has no mod stats to display!")
            return await self.interaction.response.send_message(embed=embed)
        embeds = []
        formatted_cases = get_chunks(5, CASES)
        case_num = 0
        for cases in formatted_cases:
            embed = embed_builder(author=[moderator.display_avatar.url, f"{moderator.name}'s Mod Stats"],
                                  footer=f"Total Records: {len(CASES)}")
            for case in cases:
                case_num += 1
                last_updated = "" if not case[7] else f"__Last Updated:__ {Time.parsedate(datetime.datetime.fromisoformat(case[7]))})"
                value = f"__Case ID:__ {case[0]}\n" \
                        f"__Case Type:__ {case[1].capitalize()}\n" \
                        f"__Reason:__ {case[5]}\n" \
                        f"__Issued At:__ {Time.parsedate((datetime.datetime.fromisoformat(case[6])))}{last_updated}"
                embed.add_field(name=f"Record: #{case_num}", value=value, inline=False)
            embeds.append(embed)
            if len(embeds) > 1:
                view = Paginator(pages=embeds)
                return await self.interaction.response.send_message(embed=embeds[0], view=view)
            else:
                return await self.interaction.response.send_message(embed=embeds[0])
        
    async def get_cases_for_member(self, guild: discord.Guild, member: discord.User):
        CASES = await self.db.get_cases_for_member(guild.id, member.id)
        if len(CASES) == 0:
            embed = embed_builder(description=f"{member.mention} has no cases to display!")
            return await self.interaction.response.send_message(embed=embed)
        embeds = []
        formatted_cases = get_chunks(5, CASES)
        case_num = 0
        for cases in formatted_cases:
            embed = embed_builder(author=[member.display_avatar.url, f"{member.name}'s Mod Stats"],
                                  footer=f"Total Records: {len(CASES)}")
            for case in cases:
                case_num +=1
                last_updated = "" if not case[7] else f"\nLast updated: {Time.parsedate((datetime.datetime.fromisoformat(case[7])))}"
                value = f"__Case ID:__ {case[0]}\n" \
                        f"__Case Type:__ {case[1].capitalize()}\n" \
                        f"__Reason:__ {case[5]}\n" \
                        f"__Punished at:__ {Time.parsedate((datetime.datetime.fromisoformat(case[6])))}{last_updated}"
                embed.add_field(name=f"Record: #{case_num}", value=value, inline=False)
            embeds.append(embed)
        if len(embeds) > 1:
            view = Paginator(pages=embeds)
            return await self.interaction.response.send_message(embed=embeds[0], view=view)
        else:
            return await self.interaction.response.send_message(embed=embeds[0])
    
    async def clear_cases_for_guild(self):
        TOTAL = await self.db.delete_cases_for_guild(self.interaction.guild.id)
        if TOTAL == 0:
            return embed_builder(author=[self.interaction.guild.icon.url, f"No cases to clear for {self.interaction.guild.name}"],
                                 fields=[["Total Cases:", f"{TOTAL}", True]])
        return embed_builder(author=[self.interaction.guild.icon.url, f"Cleared all cases for {self.interaction.guild.name}"], 
                             fields=[["Total Cases:", f"{TOTAL}", True]])
        
    async def clear_cases_for_member(self, member: discord.Member):
        TOTAL = await self.db.delete_cases_for_member(self.interaction.guild.id, member.id)
        if TOTAL == 0:
            return embed_builder(author=[member.display_avatar.url, f"No cases to clear for {member}"],
                                 fields=[["Total Cases:", f"{TOTAL}", True]])
        return embed_builder(author=[member.display_avatar.url, f"Cleared all cases for {member}"], 
                             fields=[["Total Cases:", f"{TOTAL}", True]])

    async def update_case(self, case_id: int, new_reason: str):
        payload = await self.db.update_case(case_id, new_reason)
        if payload:
            member = self.interaction.client.get_user(payload[0])
            old_reason = payload[1]
            return embed_builder(author=[member.display_avatar.url, f"Updated case #{case_id} for {member}"],
                                 fields=[["Updated By:", self.interaction.user], 
                                         ["Old Reason:", old_reason, False], ["New Reason:", new_reason, False]])
        return embed_builder(author=[self.interaction.guild.icon.url, f"Case #{case_id} does not exist"])
    
    async def delete_case(self, case_id: int):
        case = await self.db.delete_case(case_id)
        if case:
            case_type = case[1].capitalize()
            member = self.interaction.client.get_user(case[3])
            moderator = self.interaction.client.get_user(case[4])
            reason = case[5]
            created_at = case[6]
            last_updated = case[7]
            embed = embed_builder(author=[member.display_avatar.url, f"Deleted case #{case_id}"],
                                 fields=[["Case Type:", case_type, True], ["Offender:", str(member), True],
                                         ["Moderator:", str(moderator), True], ["Reason:", reason, True],
                                         ["Created at:", f"{Time.parsedate(datetime.datetime.fromisoformat(created_at))}", True]])
            if last_updated:
                embed.add_field(name="Last Updated:", value=f"{Time.parsedate(datetime.datetime.fromisoformat(last_updated))}", inline=True)
            return embed
        return embed_builder(author=[self.interaction.guild.icon.url, f"Case {case_id} does not exist"])
    
    async def get_case(self, case_id: int):
        case = await self.db.get_case(case_id)
        if case:
            case_type = case[1].capitalize()
            member = self.interaction.client.get_user(case[3])
            moderator = self.interaction.client.get_user(case[4])
            reason = case[5]
            created_at = case[6]
            last_updated = case[7]
            embed = embed_builder(author=[member.display_avatar.url, f"Showing case #{case_id}"],
                                 fields=[["Case Type:", case_type, True], ["Offender:", str(member), True],
                                         ["Moderator:", str(moderator), True], ["Reason:", reason, True],
                                         ["Created at:", f"{Time.parsedate(datetime.datetime.fromisoformat(created_at))}", True]])
            if last_updated:
                embed.add_field(name="Last Updated:", value=f"{Time.parsedate(datetime.datetime.fromisoformat(last_updated))}", inline=True)
            return embed
        return embed_builder(author=[self.interaction.guild.icon.url, f"Case {case_id} does not exist"])
        

def ModReason(reason):
    return "Unspecified" if not reason else reason

def TimeConverter(time: list) -> list:
    num = time[0]
    unit = time[1].lower()
    if unit == "seconds":
        seconds = num
    elif unit == "minutes":
        seconds = num*60
    elif unit == "hours":
        seconds = num*3600
    elif unit == "days":
        seconds = num*86400
    return [time, seconds]
    
def MuteTime(argument):
    time = Time.handler(argument)
    expirationDate = Time.convert_for_command(time)
    return [time, expirationDate]

@app_commands.command(name="ban", description="Ban a member from the server.")
@app_commands.describe(member="A member you want to ban.", reason="The reason for the ban")
async def ban_slash(interaction: Interaction, member: discord.Member, reason:str=None):
    reason = ModReason(reason)
    embed = embed_builder(title=f"You have been banned from {interaction.guild.name}",
                        description=f"**Reason:** {reason}\n**Banned at:** {Time.parsedate()}",
                        thumbnail=interaction.guild.icon.url)
    try: await member.send(embed=embed)
    except discord.errors.HTTPException: pass
    
    if interaction.guild.id not in [912148314223415316, 949429956843290724]:
        await interaction.guild.ban(member, reason=reason)

    log = await ModLogging(action="ban", interaction=interaction, member=member, reason=reason, expiration_date=None).handle_case(True)

    await interaction.response.send_message(embed=log if isinstance(log, discord.Embed) else log[0])

    if isinstance(log, list):
        await interaction.client.get_channel(log[1]).send(embed=log[0].add_field(name=f"Banned at:", value=f"{Time.parsedate()}", inline=False))
        
@app_commands.command(name="kick", description="Kick a member from the server.")
@app_commands.describe(member="A member you want to kick.", reason="The reason for the ban")
async def kick_slash(interaction: Interaction, member: discord.Member, reason: str=None):
    reason = ModReason(reason)
    embed = embed_builder(title=f"You have been kicked from {interaction.guild.name}",
                        description=f"**Reason:** {reason}\n**Kicked at:** {Time.parsedate()}",
                        thumbnail=interaction.guild.icon.url)
    try: await member.send(embed=embed)
    except discord.errors.HTTPException: pass
    
    if interaction.guild.id not in [912148314223415316, 949429956843290724]:
        await interaction.guild.kick(member, reason=reason)

    log = await ModLogging(action="kick", interaction=interaction, member=member, reason=reason, expiration_date=None).handle_case(True)

    await interaction.response.send_message(embed=log if isinstance(log, discord.Embed) else log[0])

    if isinstance(log, list):
        await interaction.client.get_channel(log[1]).send(embed=log[0].add_field(name=f"Kicked at:", value=f"{Time.parsedate()}", inline=False))
        
@app_commands.command(name="unban", description="Unban a member from the server.")
@app_commands.describe(member="A member you want to unban.", reason="The reason for the unban")
async def unban_slash(interaction: Interaction, member: discord.User, reason: str=None):
    reason = ModReason(reason)
    embed = embed_builder(title=f"You have been unbanned from {interaction.guild.name}",
                        description=f"**Reason:** {reason}\n**Unbanned at:** {Time.parsedate()}",
                        thumbnail=interaction.guild.icon.url)
    try: await member.send(embed=embed)
    except discord.errors.HTTPException: pass
    
    if interaction.guild.id not in [912148314223415316, 949429956843290724]:
        await interaction.guild.unban(member, reason=reason)

    log = await ModLogging(action="unban", interaction=interaction, member=member, reason=reason, expiration_date=None).handle_case(True)

    await interaction.response.send_message(embed=log if isinstance(log, discord.Embed) else log[0])

    if isinstance(log, list):
        await interaction.client.get_channel(log[1]).send(embed=log[0].add_field(name=f"Unbanned at:", value=f"{Time.parsedate()}", inline=False))
        
class Purge(app_commands.Group):
    
    @app_commands.command(name="messages", description="Purge messages in the current channel")
    async def purge_messages(self, interaction: Interaction, messages: app_commands.Range[int, 1, 100]):
        deleted = await interaction.channel.purge(limit=messages)
        embed = embed_builder(title=f"Deleted {len(deleted)} messages in #{interaction.channel.name}")
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="member", description="Purge messages from a specific member in the current channel")
    async def purge_member(self, interaction: Interaction, member: discord.User, messages: app_commands.Range[int, 1, 100]):
        deleted = await interaction.channel.purge(limit=messages, check=lambda m: m.author.id == member.id)
        embed = embed_builder(title=f"Deleted {len(deleted)} messages from {member} in #{interaction.channel.name}")
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="bot", description="Purge messages from bot accounts only in the current channel")
    async def purge_bot(self, interaction: Interaction, messages: app_commands.Range[int, 1, 100]):
        deleted = await interaction.channel.purge(limit=messages, check=lambda m: m.author.bot)
        embed = embed_builder(title=f"Deleted {len(deleted)} messages from bots in #{interaction.channel.name}")
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="after", description="Purge messages after a given message in the current channel")
    async def purge_after(self, interaction: Interaction, message: int, messages: app_commands.Range[int, 1, 100]=None):
        deleted = await interaction.channel.purge(limit=messages, after=message)
        embed = embed_builder(title=f"Deleted {len(deleted)} messages in #{interaction.channel.name}", url=message.jump_url)
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="before", description="Purge messages before a given message in the current channel")
    async def purge_before(self, interaction: Interaction, message: int, messages: app_commands.Range[int, 1, 100]=None):
        deleted = await interaction.channel.purge(limit=messages, before=message)
        embed = embed_builder(title=f"Deleted {len(deleted)} messages in #{interaction.channel.name}", url=message.jump_url)
        await interaction.response.send_message(embed=embed)
        
class Slowmode(app_commands.Group):
    
    @app_commands.command(name="on", description="Turn on slowmode for a channel")
    async def slowmode_on(self, interaction: Interaction, number: int, unit: str, channel: discord.TextChannel=None):
        duration = TimeConverter([number, unit])
        seconds = duration[1]
        channel = interaction.channel if not channel else channel
        try: await channel.edit(slowmode_delay=seconds)
        except: await interaction.response.send_message("no")
        embed = embed_builder(author=[interaction.user.display_avatar.url, f"Slowmode enabled in #{channel.name}"],
                            fields=[["Delay:", f"{number} {unit}", False]])
        await interaction.response.send_message(embed=embed)
        
    @slowmode_on.autocomplete('unit')
    async def slowmode_on_autocomplete(self, interaction: Interaction, current: str, namespace: app_commands.Namespace):
        units = ["Seconds", "Minutes", "Hours"]
        return [app_commands.Choice(name=unit, value=unit) for unit in units if current.lower() in unit.lower()]
        
    @app_commands.command(name="off", description="Turn off slowmode for a channel")
    async def slowmode_off(self, interaction: Interaction, channel: discord.TextChannel=None):
        channel = interaction.channel if not channel else channel
        if channel.slowmode_delay > 0:
            try: await channel.edit(slowmode_delay=None)
            except: await interaction.response.send_message("no")
            embed = embed_builder(author=[interaction.user.display_avatar.url, f"Slowmode disabled in #{channel.name}"])
            await interaction.response.send_message(embed=embed)
            
@app_commands.command(name="modstats", description="Display modstats for a given moderator")
async def modstats_slash(interaction: Interaction, moderator: str=None):
    moderator = interaction.user.id if not moderator else moderator
    await ModLogging(interaction=interaction).get_cases_by_moderator(interaction.client.get_user(int(moderator)))
    
@modstats_slash.autocomplete("moderator")
async def modstats_slash_autocomplete(interaction: Interaction, current: str, namespace: app_commands.Namespace):
    moderators = [[f"{member.name}#{member.discriminator}", member.id] for member in interaction.guild.members if member.guild_permissions.manage_messages and not member.bot]
    return [app_commands.Choice(name=moderator[0], value=str(moderator[1])) for moderator in moderators if current.lower() in moderator[0].lower()]

class Cases(app_commands.Group):
    
    clear = app_commands.Group(name="clear", description="Clear all cases for the server or a member")
    
    @app_commands.command(name="display", description="Display all cases for a given member")
    async def cases_display_slash(self, interaction: Interaction, member: discord.Member=None):
        member = interaction.user if not member else member
        await ModLogging(interaction=interaction).get_cases_for_member(interaction.guild, member)
    
    @clear.command(name="server", description="Clear all cases for the entire server")
    async def clear_cases_guild_slash(self, interaction: Interaction):
        embed = await ModLogging(interaction=interaction).clear_cases_for_guild()
        await interaction.response.send_message(embed=embed)
    
    @clear.command(name="member", description="Clear all cases for a specific member")
    async def clear_cases_member_slash(self, interaction: Interaction, member: discord.Member):
        embed = await ModLogging(interaction=interaction).clear_cases_for_member(member)
        await interaction.response.send_message(embed=embed)
    
class Case(app_commands.Group):
    
    @app_commands.command(name="edit", description="Edit a reason for a given case")
    async def case_edit_slash(self, interaction: Interaction, case_id: int, new_reason: str):
        embed = await ModLogging(interaction=interaction).update_case(case_id, new_reason)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="remove", description="Delete a given case")
    async def case_remove_slash(self, interaction: Interaction, case_id: int):
        embed = await ModLogging(interaction=interaction).delete_case(case_id)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="display", description="Display info for a given case")
    async def case_display_slash(self, interaction: Interaction, case_id: int):
        embed = await ModLogging(interaction=interaction).get_case(case_id)
        await interaction.response.send_message(embed=embed)
    
        
def setup(bot: discord.Client):
    commands = [ban_slash, kick_slash, unban_slash, Purge(), Slowmode(), modstats_slash, Cases(), Case()]
    guilds = [912148314223415316, 949429956843290724]
    for command in commands:
        for guild in guilds:
            bot.tree.add_command(command, guild=discord.Object(guild))
        print(f"Added {command.name} to both guilds")