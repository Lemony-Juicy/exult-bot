import datetime
from operator import mod

class CasesDB:
    def __init__(self, db):
        self.db = db
        self.conn = self.db.get_connection
        
    async def add_case(self, case_type: str, guild_id: int, user_id: int, moderator_id: int, reason: str, expiration_date: str, return_case:bool):
        conn = await self.conn()
        await conn.execute("INSERT INTO cases(case_type, guild_id, user_id, moderator_id, reason, created_at, expiration_date) " \
                           "VALUES ($1, $2, $3, $4, $5, $6, $7)", case_type, guild_id, user_id, moderator_id, reason, 
                                                                    str(datetime.datetime.utcnow()), expiration_date)
        if return_case:
            cases = await conn.fetch("SELECT count(*) FROM cases WHERE guild_id = $1", guild_id)
            await conn.close()
            return cases[0][0]
        await conn.close()
        
    async def get_case(self, case_id: int):
        conn = await self.conn()
        case = await conn.fetchrow("SELECT * FROM cases WHERE case_id = $1", case_id)
        await conn.close()
        return case
        
    async def get_cases_by_moderator(self, moderator_id: int):
        conn = await self.conn()
        cases = await conn.fetch("SELECT * FROM cases WHERE moderator_id = $1", moderator_id)
        await conn.close()
        return cases
    
    async def get_cases_for_member(self, guild_id: int, user_id: int, case_type: str=None):
        conn = await self.conn()
        if case_type:
            cases = await conn.fetch("SELECT * FROM cases WHERE guild_id=$1 AND user_id=$2 AND case_type=$3", guild_id, user_id, case_type)
        elif not case_type:
            cases = await conn.fetch("SELECT * FROM cases WHERE guild_id = $1 AND user_id = $2", guild_id, user_id)
        await conn.close()
        return cases
        
    async def delete_cases_for_guild(self, guild_id: int):
        conn = await self.conn()
        total = await conn.fetch("SELECT COUNT(*) FROM cases WHERE guild_id=$1", guild_id)
        await conn.execute("DELETE FROM cases WHERE guild_id=$1", guild_id)
        await conn.close()
        return total[0][0]
    
    async def delete_cases_for_member(self, guild_id: int, user_id: int):
        conn = await self.conn()
        total = await conn.fetch("SELECT COUNT(*) FROM cases WHERE guild_id=$1 and user_id=$2", guild_id, user_id)
        await conn.execute("DELETE FROM cases WHERE guild_id=$1and user_id=$2", guild_id, user_id)
        await conn.close()
        return total[0][0]
    
    async def update_case(self, case_id: int, reason: str):
        conn = await self.conn()
        case = await self.get_case(case_id)
        case_reason = case[5]
        case_member = case[3]
        await conn.execute("UPDATE cases SET reason=$1 WHERE case_id=$2", reason, case_id)
        await conn.execute("UPDATE cases SET last_updated=$1 WHERE case_id=$2", str(datetime.datetime.utcnow()), case_id)
        await conn.close()
        return [case_member, case_reason]
    
    async def delete_case(self, case_id: int):
        conn = await self.conn()
        case = await self.get_case(case_id)
        await conn.execute("DELETE FROM cases WHERE case_id = $1", case_id)
        await conn.close()
        return case