import discord
from discord.ext import commands
import kimetsu
#Discord related imports

from waifuim import WaifuAioClient
import asyncio
import asyncpg
import logging
import time
import os
import aiohttp
import json
import nest_asyncio
nest_asyncio.apply()
#Regular Imports

import config
from database import db
from database.prefix import PrefixDB
from tools.components import SuggestVotes
from cogs.friends import Abberantics
from cogs.ac.s_slashtest import SlashTest
#Local file imports

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

ignore_exts = ["currency.py", "games.py", "tickets.py"]
exts = [file for file in os.listdir("cogs") if file.endswith(".py") and not file.startswith("_") and not file.startswith("s_") and not file.startswith("u_") and file not in ignore_exts]
aexts = ["cogs.ac.s_slashtest", "cogs.ac.u_usertest"]

async def get_prefix(bot, msg):
    try:
        con = PrefixDB(bot.db)
        result = await con.get(msg.guild.id)
        prefix = commands.when_mentioned_or(result.get("prefix"))(bot, msg)
        return prefix
    except:
        return "e!"

class Exult(commands.AutoShardedBot):
    def __init__(self):
        self.startTime = time.time()
        self.__version__ = "0.0.1"
        super().__init__(
            activity=discord.Activity(type=discord.ActivityType.watching, name="Verification Coming Soon!"),
            command_prefix=(get_prefix),
            description="A general purpose bot for any server!",
            intents=discord.Intents.all(),
        )
        self.db = db.Database()
        self.logger = logging.getLogger(__name__)
        self.owner_ids=[]

    async def _init(self):
        connection = self.db.get_connection()
        self.pool = connection.pool
    
    async def setup(self):
        #await self.http.bulk_upsert_guild_commands(self.user.id, 912148314223415316, [])
        for ext in exts: self.load_extension(f"cogs.{ext[:-3]}") #Cogs
        for aext in aexts:
            self.load_extension(aext)
        self.load_extension("jishaku")
        await super().setup()
        
    def parsedate(self, date=None):
        kimetsu.Time.parsedate(date)

    def formatdate(self, date=None):
        kimetsu.Time.formatdate(date)
        
    async def get_latency(self):
        _ = []
        for x in range(3):
            x = time.time()
            await self.pool.execute("SELECT * FROM latency_test")
            y = time.time()
            _.append(y-x)
        return (_[0] + _[1] + _[2]) / 3

    async def emoji(self):
        emoji = self.get_emoji(936464383343738910)
        return emoji
        
    arrow = "<a:arrow:882812954314154045>"
    red = 0xfb5f5f
    green = 0x2ecc71
    gold = 0xf1c40f
    invis = '\u200b'
    invite = "https://discord.com/api/oauth2/authorize?client_id=889185777555210281&permissions=3757567166&scope=bot%20applications.commands"
    persistent_views_added = False
    

    async def on_ready(self):
        print(f"Loaded {len(self.cogs)} cogs, with {len(self.all_commands)} commands.")
        if not self.persistent_views_added:
            self.add_view(SuggestVotes(self))
            self.add_view(Abberantics.VerifyButton(self))
            print("Persistent views added")
            self.persistent_views_added = True
            print(f"Successfully logged in to {self.user}. ({round(self.latency*1000)}ms)")
            print(f"Startup time: {round(time.time() - bot.startTime)}s")

bot = Exult()
bot.loop = asyncio.get_event_loop()
bot.remove_command("help")

async def run_bot():
    try:
        bot.pool = await asyncpg.create_pool(config.PSQL_URI)
        print(f"Database Pool Created. ({round(await bot.get_latency()*1000, 2)}ms)")
        bot.session = aiohttp.ClientSession()
        print("Aiohttp Session Started.")
        bot.wf = WaifuAioClient(appname="Exult", session=bot.session)
        print("Waifu Client Started.")
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
    await bot.session.close()
    bot.logger.info("Bot AIOHTTP client session closed")

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
    with open(file) as f:
        data = json.load(f)
    data[key] = writeData
    with open(file, 'w') as f:
        json.dump(data, f)


bot.run(config.TOKEN)
