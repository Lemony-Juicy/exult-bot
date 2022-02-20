from ast import literal_eval
import json
from datetime import datetime, timedelta
import discord

class GuildConfigDB:
    def __init__(self, db):
        self.db = db

        
    async def check_guild(self, guild_id: int):
        conn = await self.db.get_connection()
        x = await conn.fetch("SELECT * FROM guild_config WHERE guild_id=$1", guild_id)
        await conn.close()
        if len(x) < 1:
            return "No records of this guild on database"
        return x[0]

    async def get_conf(self, guild_id: int, attr):
        conn = await self.db.get_connection()
        x = await conn.fetchrow("SELECT config FROM guild_config WHERE guild_id = $1", guild_id)
        await conn.close()
        config = literal_eval(x[0])
        try:
            conf_attr = config[attr]
        except KeyError:
            return None
        return conf_attr
    
    async def get_module(self, guild_id: int):
        conn = await self.db.get_connection()
        x = await conn.fetchrow("SELECT modules FROM guild_config WHERE guild_id = $1", guild_id)
        await conn.close()
        modules = literal_eval(x[0])
        return modules

    async def add_conf(self, guild_id: int, attr: str, attr_id):
        conn = await self.db.get_connection()
        config = await self.get_conf(guild_id)
        configuration = literal_eval(config[0])
        configuration[attr] = attr_id
        await conn.execute("UPDATE guild_config SET config = $1 WHERE guild_id = $2", f"{configuration}", guild_id)
        await conn.close()

    async def add_guild(self, guild: discord.Guild):
        conn = await self.db.get_connection()
        guild_text = {}
        guild_voice = {}
        guild_roles = {}
        for tchan in guild.text_channels:
            guild_text[tchan.name] = tchan.id
        for vchan in guild.voice_channels:
            guild_voice[vchan.name] = vchan.id
        for role in guild.roles:
            guild_roles[role.name] = [role.id, str(role.color)]
        guildtext = json.dumps(guild_text)
        guildvoice = json.dumps(guild_voice)
        del guild_roles["@everyone"]
        guildroles = json.dumps(guild_roles)
        guildconfig = json.dumps({'prefix': 'e!'})
        guildmodules = json.dumps({'ban': True})
        await conn.execute("INSERT INTO guild_config(guild_id, guild_name, guild_members, guild_text, guild_voice, guild_roles, "
                           "config, modules) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)", guild.id, guild.name, len(guild.members),
                           guildtext, guildvoice, guildroles, guildconfig, guildmodules)
        await conn.close()

    async def remove_guild(self, guild_id: int):
        conn = await self.db.get_connection()
        await conn.execute("DELETE FROM guild_config WHERE guild_id=$1", guild_id)
        await conn.close()
    
    async def add_bot_removed(self, guild_id):
        conn = await self.db.get_connection()
        expiryDate = datetime.utcnow() + timedelta(days=30)
        await conn.execute("UPDATE guild_config SET bot_removed=$1 WHERE guild_id=$2", str(expiryDate), guild_id)
        
    async def remove_bot_removed(self, guild_id):
        conn = await self.db.get_connection()
        await conn.execute("UPDATE guild_config SET bot_removed=$1 WHERE guild_id=$2", None, guild_id)
        
    async def get_outdated_configs(self):
        conn = await self.db.get_connection()
        try:
            x = await conn.fetch("SELECT * FROM guild_config WHERE bot_removed <= $1", str(datetime.datetime.utcnow()))
        except:
            return None
        await conn.close()
        return x
    
    async def add_every_guild(self, guilds: list):
        for guild in guilds:
            await self.add_guild(guild)
        print("Added all guilds to db")
        
    async def update_guild_name(self, guild: discord.Guild):
        conn = await self.db.get_connection()
        await conn.execute("UPDATE guild_config SET guild_name = $1 WHERE guild_id=$2", guild.name, guild.id)
        await conn.close()
        
    async def update_guild_members(self, guild: discord.Guild):
        conn = await self.db.get_connection()
        await conn.execute("UPDATE guild_config SET guild_members = $1 WHERE guild_id=$2", len(guild.members), guild.id)
        await conn.close()
        
    async def update_guild_text(self, guild: discord.Guild):
        conn = await self.db.get_connection()
        await conn.execute("UPDATE guild_config SET guild_text = $1 WHERE guild_id=$2", len(guild.text_channels), guild.id)
        await conn.close()
        
    async def update_guild_voice(self, guild: discord.Guild):
        conn = await self.db.get_connection()
        await conn.execute("UPDATE guild_config SET guild_voice = $1 WHERE guild_id=$2", len(guild.voice_channels), guild.id)
        await conn.close()
        
    async def update_guild_roles(self, guild: discord.Guild):
        conn = await self.db.get_connection()
        await conn.execute("UPDATE guild_config SET guild_roles = $1 WHERE guild_id=$2", len(guild.roles), guild.id)
        await conn.close()