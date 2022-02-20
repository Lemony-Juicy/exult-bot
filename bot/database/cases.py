import datetime

class CasesDB:
    def __init__(self, db):
        self.db = db

    async def add_case(self, case_type, guild_id, user_id, moderator_id, reason, expiration_date):
        conn = await self.db.get_connection()
        await conn.execute("INSERT INTO cases" \
                           "(case_type, guild_id, user_id, moderator_id, reason, created_at, expiration_date) " \
                           "VALUES ($1, $2, $3, $4, $5, $6, $7)", case_type, guild_id, user_id,
                                                              moderator_id, reason, str(datetime.datetime.utcnow()), expiration_date)
        await conn.close()

    async def get_case(self, case_id):
        conn = await self.db.get_connection()
        x = await conn.fetchrow("SELECT * FROM cases WHERE case_id = $1", case_id)
        await conn.close()
        return x

    async def get_cases_by_moderator(self, moderator_id):
        conn = await self.db.get_connection()
        x = await conn.fetch("SELECT * FROM cases WHERE moderator_id = $1", moderator_id)
        await conn.close()
        return x

    async def get_cases_for_member(self, guild_id, user_id, case_type=None):
        conn = await self.db.get_connection()
        if case_type:
            x = await conn.fetch("SELECT * FROM cases WHERE guild_id=$1 AND user_id=$2 AND case_type=$3", guild_id, user_id, case_type)
        elif not case_type:
            x = await conn.fetch("SELECT * FROM cases WHERE guild_id = $1 AND user_id = $2", guild_id, user_id)
        await conn.close()
        return x

    async def update_case(self, case_id, reason):
        conn = await self.db.get_connection()
        await conn.execute("UPDATE cases SET reason=$1 WHERE case_id=$2", reason, case_id)
        await conn.execute("UPDATE cases SET last_updated=$1 WHERE case_id=$2", str(datetime.datetime.utcnow()), case_id)
        await conn.close()

    async def remove_case(self, case_id):
        conn = await self.db.get_connection()
        await conn.execute("DELETE FROM cases WHERE case_id=$1", case_id)
        await conn.close()

    async def clear_member(self, guild_id, user_id, case_type=None):
        conn = await self.db.get_connection()
        if case_type:
            await conn.execute("DELETE FROM cases WHERE guild_id = $1 AND user_id = $2 AND case_type=$3", guild_id, user_id, case_type)
        if not case_type:
            await conn.execute("DELETE FROM cases WHERE guild_id = $1 AND user_id = $2", guild_id, user_id)
        await conn.close()

    async def clear_guild(self, guild_id, case_type=None):
        conn = await self.db.get_connection()
        if case_type:
            x = await conn.fetch("SELECT * FROM cases WHERE guild_id = $1 AND case_type=$2", guild_id, case_type)
            await conn.execute("DELETE FROM cases WHERE guild_id = $1 AND case_type=$2", guild_id, case_type)
        if not case_type:
            x = await conn.fetch("SELECT * FROM cases WHERE guild_id = $1", guild_id)
            await conn.execute("DELETE FROM cases WHERE guild_id = $1", guild_id)
        await conn.close()
        return len(x)

    async def case_end(self, case_id):
        conn = await self.db.get_connection()
        await conn.execute("UPDATE cases SET expiration_date = $1 WHERE case_id = $2", None, case_id)
        await conn.execute("UPDATE cases SET last_updated=$1 WHERE case_id=$2", str(datetime.datetime.utcnow()), case_id)
        await conn.close()

    async def get_outdated(self):
        conn = await self.db.get_connection()
        try:
            x = await conn.fetch("SELECT * FROM cases WHERE expiration_date <= $1", str(datetime.datetime.utcnow()))
        except:
            return None
        await conn.close()
        return x
