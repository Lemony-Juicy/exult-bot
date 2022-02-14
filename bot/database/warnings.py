class WarningDB:
    def __init__(self, db):
        self.db = db

    async def add_warn(self, guild_id, user_id, moderator_id, reason):
        conn = await self.db.get_connection()
        await conn.execute("INSERT INTO warnings(guild_id, user_id, moderator_id, reason) VALUES ($1, $2, $3, $4)", guild_id, user_id, moderator_id, reason)
        await conn.close()

    async def get_warn(self, warning_id):
        conn = await self.db.get_connection()
        x = await conn.fetchrow("SELECT * FROM warnings WHERE warning_id = $1", warning_id)
        await conn.close()
        return x

    async def get_warns_by_moderator(self, moderator_id):
        conn = await self.db.get_connection()
        x = await conn.fetch("SELECT * FROM warnings WHERE moderator_id = $1", moderator_id)
        await conn.close()
        return x

    async def get_warns_for_member(self, guild_id, user_id):
        conn = await self.db.get_connection()
        x = await conn.fetch("SELECT * FROM warnings WHERE guild_id = $1 AND user_id = $2", guild_id, user_id)
        await conn.close()
        return x
    
    async def update(self, warning_id, reason):
        conn = await self.db.get_connection()
        await conn.execute("UPDATE warnings SET reason=$1 WHERE warning_id=$2", reason, warning_id)
        await conn.close()
    
    async def remove(self, warning_id):
        conn = await self.db.get_connection()
        await conn.execute("DELETE FROM warnings WHERE warning_id=$1", warning_id)
        await conn.close()

    async def clear_member(self, guild_id, user_id):
        conn = await self.db.get_connection()
        await conn.execute("DELETE FROM warnings WHERE guild_id = $1 AND user_id = $2",guild_id, user_id)
        await conn.close()

    async def clear_guild(self, guild_id):
        conn = await self.db.get_connection()
        x = await conn.fetch("SELECT * FROM warnings WHERE guild_id = $1", guild_id)
        await conn.execute("DELETE FROM warnings WHERE guild_id = $1", guild_id)
        await conn.close()
        return len(x)