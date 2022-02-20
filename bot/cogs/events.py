from database.leveling import LevelingDB
import discord
from discord.ext import commands

from kimetsu import embed
from database.prefix import PrefixDB
from database.logs import LogsDB
from database.config import GuildConfigDB

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
    async def on_guild_join(self, guild: discord.Guild):
        embed = discord.Embed(title="New server joined!", description=f"**Server:** `{guild.name}`\n**Members:** {len(guild.members)}", colour=discord.Colour.green()).set_footer(text=f"ID: {guild.id}").set_author(icon_url=self.bot.user.display_avatar.url, name=f"Total guilds: {len(self.bot.guilds)}")
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await self.bot.get_channel(914193452428836884).send(embed=embed)

        con = PrefixDB(self.bot.db)
        await con.add(guild.id, "e!")

        con = LogsDB(self.bot.db)
        await con.add_guild(guild.id)
        
        con = GuildConfigDB(self.bot.db)
        await con.remove_bot_removed(guild.id)
        await con.add_guild(guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        if not hasattr(guild, "member_count"):
            return
        embed = discord.Embed(title="Removed from server!", description=f"**Server:** `{guild.name}`\n**Members:** {len(guild.members)}", colour=discord.Colour.red()).set_footer(text=f"ID: {guild.id}").set_author(icon_url=self.bot.user.display_avatar.url, name=f"Total guilds: {len(self.bot.guilds)}")
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        con = PrefixDB(self.bot.db)
        await con.remove(guild.id)

        con = LogsDB(self.bot.db)
        await con.rem_guild(guild.id)
        
        con = GuildConfigDB(self.bot.db)
        await con.add_bot_removed(guild.id)

        await self.bot.get_channel(914193452428836884).send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot: return
        if not message.guild: return
        con = PrefixDB(self.bot.db)
        prefix = await con.get(message.guild.id)
        prefix = prefix[0]
        if message.content == "<@!889185777555210281>":
            await message.reply(f"My prefix is: `{prefix}`")
        if message.content.startswith("v!") and prefix == "e!":
            await message.reply("My prefix is no longer `v!`, it is now `e!`. If you'd like to change it to something else you can do `e!config prefix <new_prefix>`!")
        if message.guild.id in [336642139381301249, 744484300694487050, 514232441498763279]:
            return
        if message.guild:
            if message.guild.id == 912148314223415316:
                await self.Client.add_xp(message.author, message)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        x = LevelingDB(self.bot.db)
        await x.insert(member.id, member.guild.id, 0, 1)
        await GuildConfigDB(self.bot.db).update_guild_members(member.guild)
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await GuildConfigDB(self.bot.db).update_guild_members(member.guild)
        
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if before.name != after.name:
            await GuildConfigDB(self.bot.db).update_guild_name(after)
            
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        if channel.type == 'text':
            await GuildConfigDB(self.bot.db).update_guild_text(channel.guild)
        elif channel.type == 'voice':
            await GuildConfigDB(self.bot.db).update_guild_voice(channel.guild)
        
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        if channel.type == 'text':
            await GuildConfigDB(self.bot.db).update_guild_text(channel.guild)
        elif channel.type == 'voice':
            await GuildConfigDB(self.bot.db).update_guild_voice(channel.guild)
            
    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        await GuildConfigDB(self.bot.db).update_guild_roles(role.guild)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        await GuildConfigDB(self.bot.db).update_guild_roles(role.guild)
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=discord.Embed(description=error, colour=self.bot.red))
        else:
            print(error)
        
def setup(bot):
    bot.add_cog(Events(bot))
