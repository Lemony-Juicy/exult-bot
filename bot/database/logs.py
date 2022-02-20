class LogsDB:
    def __init__(self, db):
        self.db = db

    async def add_guild(self, guild_id):
        conn = await self.db.get_connection()
        await conn.execute("INSERT INTO logs(guild_id) VALUES ($1)", guild_id)
        await conn.close()

    async def rem_guild(self, guild_id):
        conn = await self.db.get_connection()
        await conn.execute("DELETE FROM logs WHERE guild_id=$1", guild_id)
        await conn.close()
    
    async def get(self, guild_id, event):
        conn = await self.db.get_connection()
        x = await conn.fetchrow(f"SELECT {event} FROM logs WHERE guild_id=$1", guild_id)
        await conn.close()
        return x[0]

    async def add(self, guild_id, event, channel_id):
        conn = await self.db.get_connection()
        await conn.execute(f"UPDATE logs SET {event}=$1 WHERE guild_id=$2", channel_id, guild_id)
        await conn.close()
    
    async def update(self, guild_id, event, channel_id):
        await self.add(guild_id, event, channel_id)
    
    async def remove(self, guild_id, event):
        conn = await self.db.get_connection()
        await conn.execute(f"UPDATE logs SET {event}=$1 WHERE guild_id=$2", None, guild_id)
        await conn.close()