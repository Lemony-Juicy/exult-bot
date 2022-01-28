import discord
from discord.ext import commands
import kimetsu

from datetime import datetime
import asyncio
import asyncpg
import logging
import time
import os
import aiohttp

import config
from database import db
from database.prefix import PrefixDB
from info import cogs
import json

from waifuim import WaifuAioClient

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

async def get_prefix(bot, msg):
    con = PrefixDB(bot.db)
    result = await con.get(msg.guild.id)
    prefix = commands.when_mentioned_or(result.get("prefix"))(bot, msg)
    return prefix

class Exult(commands.AutoShardedBot):
    def __init__(self):
        self.__version__ = "0.0.1"
        super().__init__(
            activity=discord.Activity(type=discord.ActivityType.watching, name="Verification Coming Soon!"),
            command_prefix=(get_prefix),
            description="A general purpose bot for any server!",
            intents=discord.Intents.all(),
            slash_commands=True
        )
        self.db = db.Database()
        self.logger = logging.getLogger(__name__)
        self.owner_ids=[]

    async def _init(self):
        connection = self.db.get_connection()
        self.pool = connection.pool
    
    async def setup(self):
        for ext in cogs.exts: self.load_extension(ext)
        await self.create_slash_commands()
        
    def parsedate(self, date=None):
        kimetsu.Parsedate(date).parsedate()

    def formatdate(self, date=None):
        kimetsu.Formatdate.formatdate(date)
        
    async def get_latency(self):
        _ = []
        for x in range(3):
            x = time.time()
            await self.pool.execute("SELECT * FROM latency_test")
            y = time.time()
            _.append(y-x)
        return (_[0] + _[1] + _[2]) / 3
        
    arrow = "<a:arrow:882812954314154045>"
    red = 0xfb5f5f
    wf = WaifuAioClient(appname="Varietas")

bot = Exult()
bot.loop = asyncio.get_event_loop()
bot.remove_command("help")


async def run_bot():
    try:
        bot.pool = await asyncpg.create_pool(config.PSQL_URI)
    except (ConnectionError, asyncpg.exceptions.CannotConnectNowError):
        bot.logger.critical("Could not connect to psql.")
        
async def close_bot():
    await bot.pool.close()
    bot.logger.info("Closed psql connection")
    await bot.close()
    bot.logger.info("logged out of bot")
    await bot.http.close()
    bot.logger.info("HTTP Session closed")
    for task in asyncio.all_tasks(loop=bot.loop):
        task.cancel()
        bot.logger.info("Cancelled running task")

try:
    bot.loop.run_until_complete(run_bot())
except KeyboardInterrupt:
    bot.loop.run_until_complete(close_bot())


def getIntDict(D):
    data = {}
    for key in D.copy().keys():
        k = int(key)
        data[k] = D[key]
    return data


def read(file, key, i=2, isDict=True):
    """Gain data from json file"""
    with open(file) as data:
        try:
            full = json.load(data)[key]
            if not isDict:
                return full
        except KeyError:
            return {} if isDict else []
    if i == 0:
        return full
    full = getIntDict(full)
    if i == 1:
        return full
    data = {}
    for key in full.copy().keys():
        data[key] = getIntDict(full[key])
    return data


def write(file, writeData, key):
    """write data to json file"""
    with open(file) as f:
        data = json.load(f)
    data[key] = writeData
    with open(file, 'w') as f:
        json.dump(data, f)

bot.run(config.TOKEN)
