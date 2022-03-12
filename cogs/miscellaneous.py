import discord
from discord import app_commands, Interaction

from utils import *
from database import *

@app_commands.command(name="avatar", description="Get a user's avatar and banner")
@app_commands.describe(member="A member whose avatar/banner you want to view.")
async def avatar_slash(interaction: Interaction, member:discord.Member=None):
    member = interaction.user if not member else member
    embed = embed_builder(author=[member.display_avatar.url, f"{member.name}'s Avatar"],
                          image=member.display_avatar.url)
    member = await interaction.client.fetch_user(member.id)
    if member.banner:
        view = Avatar(member)
        return await interaction.response.send_message(embed=embed, view=view)
    await interaction.response.send_message(embed=embed)
    
class Role(app_commands.Group):
    
    @app_commands.command(name="info", description="Display info on a given role")
    @app_commands.describe(role="The role you want to display info on")
    async def role_info_slash(self, interaction: Interaction, role:discord.Role):
            Permissions = []
            if role.permissions.administrator:
                Permissions.append("Administrator")
            if role.permissions.ban_members:
                Permissions.append("Ban Members")
            if role.permissions.deafen_members:
                Permissions.append("Server Deafen Members")
            if role.permissions.kick_members:
                Permissions.append("Kick Members")
            if role.permissions.manage_channels:
                Permissions.append("Manage Channels")
            if role.permissions.manage_emojis:
                Permissions.append("Manage Emojis")
            if role.permissions.manage_guild:
                Permissions.append("Manage Server")
            if role.permissions.manage_messages:
                Permissions.append("Manage Messages")
            if role.permissions.manage_nicknames:
                Permissions.append("Manage Nicknames")
            if role.permissions.manage_permissions:
                Permissions.append("Manage Permissions")
            if role.permissions.manage_roles:
                Permissions.append("Manage Roles")
            if role.permissions.manage_webhooks:
                Permissions.append("Manage Webhooks")
            if role.permissions.mention_everyone:
                Permissions.append("Mention Everyone")
            if role.permissions.move_members:
                Permissions.append("Move Members")
            if role.permissions.mute_members:
                Permissions.append("Server Mute Members")
            if role.permissions.view_audit_log:
                Permissions.append("View Audit Log")
            if len(Permissions) == 0:
                Permissions = "No special permissions"
            elif Permissions[0] == "Administrator":
                Permissions = Permissions[0]
            else:
                Permissions = str(Permissions)
                Permissions = Permissions.replace("'", "").replace("[", "").replace("]", "")
            embed = embed_builder(colour=role.colour, 
                                author=f"Role Info: {role.name}",
                                thumbnail=None if not role.icon else role.icon.url,
                                fields=[
                                    ["ID:", str(role.id), True],
                                    ["Name:", role.name, True],
                                    ["Colour:", role.colour, True],
                                    ["Mention:", role.mention, True],
                                    ["Hoisted:", "Yes" if role.hoist else "No", True],
                                    ["Position:", str(role.position), True],
                                    ["Mentionable:", "Yes" if role.mentionable else "No"],
                                    ["Created At:", Time.parsedate(role.created_at), True],
                                    ["Members with role:", len(role.members), True],
                                    ["Important Permissions:", Permissions, False]
                                ])
            await interaction.response.send_message(embed=embed)
            
    @app_commands.command(name="members", description="Display all members with a given role.")
    @app_commands.describe(role="The role you want to view members for.")
    async def role_members_slash(self, interaction: Interaction, role: discord.Role):
        formatted_members = get_chunks(20, sorted([str(member) for member in role.members]))
        embeds = []
        for members in formatted_members:
            embed = embed_builder(title=f"Members with {role.name}",
                                footer=f"Total Members with {role.name}: {len(role.members)}",
                                thumbnail=None if not role.icon else role.icon.url)
            for member in members:
                if not embed.description:
                    embed.description = f"{member}\n"
                else:
                    embed.description += f"{member}\n"
            embeds.append(embed)
        if len(embeds) > 1:
            view = Paginator(pages=embeds)
            return await interaction.response.send_message(embed=embeds[0], view=view)
        await interaction.response.send_message(embed=embeds[0])
        
@app_commands.command(name="serverinfo", description="Display info on the current server.")
async def serverinfo_slash(interaction: Interaction):
    guild = interaction.guild
    statuses = [len(list(filter(lambda m: str(m.status) == "online", guild.members))),
                len(list(filter(lambda m: str(m.status) == "idle", guild.members))),
                len(list(filter(lambda m: str(m.status) == "dnd", guild.members))),
                len(list(filter(lambda m: str(m.status) == "offline", guild.members)))]
    embed = embed_builder(author=f"Server Info: {guild.name}",
                          footer=f"Server ID: {guild.id}",
                          thumbnail=None if not guild.icon else guild.icon.url,
                          fields=[
                              ["Owner:", guild.owner, True], ["Created At:", Time.parsedate(guild.created_at), True],
                              ["Members:", len([member for member in guild.members if not member.bot]), True],
                              ["Bots:", len([member for member in guild.members if member.bot]), True],
                              ["Banned Members:", len(await guild.bans()), True], ["Roles", len(guild.roles), True],
                              ["Categories:", len(guild.categories), True], ["Text Channels:", len(guild.text_channels), True],
                              ["Voice Channels:", len(guild.voice_channels), True], ["Nitro Boosts:", guild.premium_subscription_count, True],
                              ["Booster Level:", guild.premium_tier, True], ["Invites", len(await guild.invites()), True],
                              ["Statuses:", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", False]
                          ])
    await interaction.response.send_message(embed=embed)

@app_commands.command(name="userinfo", description="Display info on a given member.")
@app_commands.command(member="The member you want to display info for.")
async def userinfo_slash(interaction: Interaction, member: discord.Member):
    if str(member.status) == "dnd":
        status = "🔴 DND"
    elif str(member.status) == "online":
        status = "🟢 Online"
    elif str(member.status) == "offline":
        status = "⚫ Offline"
    elif str(member.status) == "idle":
        status = "🟠 Idle"
    elif str(member.status) == "streaming":
        status = "🟣 Streaming"
        
    badges_str = "" if not member.public_flags.hypesquad_balance() else "<:Balance:951943457193214014>  "
    badges_str += "" if not member.public_flags.hypesquad_bravery() else "<:Bravery:951943457738477608>  "
    badges_str += "" if not member.public_flags.hypesquad_brilliance() else "<:Brilliance:951943457214169160>  "
    badges_str += "" if not member.public_flags.hypesquad() else "<:Hypesquad:951943457700720660>  "
    badges_str += "" if not member.public_flags.early_supporter() else "<:EarlySupporter:951943457621028864>  "
    badges_str += "" if not member.public_flags.bug_hunter() else "<:BugHunter:951943457511964792>  "
    badges_str += "" if not member.public_flags.bug_hunter_level_2() else "<:BugHunter2:951943457629405264>  "
    badges_str += "" if not member.public_flags.partner() else "<:DiscordPartner:951943457495207986>  "
    badges_str += "" if not member.public_flags.staff() else "<:DiscordStaff:951943457721700402>  "
    badges_str += "" if not member.public_flags.early_verified_bot_developer() else "<:EarlyVerifiedBotDev:951943458174689391>  "
    badges_str += "" if not member.public_flags.discord_certified_moderator() else "<:DiscordCertifiedModerator:951945202963198062>  "
    badges_str += "" if not member.public_flags.verified_bot() else "<:VerifiedBot:951943457788813363>  "
    
    roles = ""
    if len(member.roles) > 1:
        for role in member.roles[1:].reverse():
            roles += f"{role.mention}, "
    roles = "Member has no roles" if roles == "" else roles
    
    
def setup(bot):
    commands = [avatar_slash, Role(), serverinfo_slash, ]
    guilds = [912148314223415316, 949429956843290724]
    for command in commands:
        for guild in guilds:
            bot.tree.add_command(command, guild=discord.Object(guild))
        print(f"Added {command.name} to both guilds")
        