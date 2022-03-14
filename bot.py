import discord
from discord import app_commands
from discord.ext import commands
#Discord Related Imports

from dotenv import load_dotenv
import os
import logging
from time import time
import asyncpg
import aiohttp
from waifuim import WaifuAioClient
import asyncio
from typing import Literal, List
#Regular Imports

from database import *
#Local Imports

load_dotenv()
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
TOKEN = os.environ["TEST_TOKEN"]

class ExultTest(commands.Bot):
    def __init__(self):
        self.startTime = time()
        self.__version__ = "0.2"
        self.db = Database()
        self.logger = logging.getLogger(__name__)
        self.owner_id = [839248459704959058]
        super().__init__(
            activity=discord.Activity(type=discord.ActivityType.watching, name="Exult Rewrite"),
            command_prefix="t!",
            description="An all-in-one bot to fit all your needs. Moderation, Fun, Utility and More!",
            intents=discord.Intents.all()
        )
        
    async def _init(self):
        connection = self.db.get_connection()
        self.pool = connection.pool
        
    async def setup_hook(self):
        exts = [f"cogs.{file[:-3]}" for file in os.listdir("cogs") if file.endswith(".py") and not file.startswith("_")]
        exts.insert(0, "jishaku")
        for ext in exts: self.load_extension(ext)
        
        
    async def get_latency(self):
        _ = []
        for x in range(3):
            x = time()
            await self.pool.execute("SELECT * FROM latency_test")
            y = time()
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
        for guild in [912148314223415316, 949429956843290724]:
            await self.tree.sync(guild=discord.Object(id=guild))
        print(f"Loaded {len(self.cogs)} cogs, with {len(self.all_commands)} commands.")
        if not self.persistent_views_added:
            #print("Persistent views added")
            self.persistent_views_added = True
            print(f"Successfully logged in to {self.user}. ({round(self.latency*1000)}ms)")
            print(f"Startup time: {round(time() - self.startTime)}s")
            
bot = ExultTest()
#bot.remove_command("help")

async def run_bot():
    try:
        bot.pool = await asyncpg.create_pool(os.environ["PSQL_URI"])
        bot.logger.info(f"Database Pool Created. ({round(await bot.get_latency()*1000, 2)}ms)")
        bot.session = aiohttp.ClientSession()
        bot.logger.info("Aiohttp Session Created Successfully")
        bot.wf = WaifuAioClient(session=bot.session, appname="Exult")
        bot.logger.info("Waifu Client Started")
    except (ConnectionError, asyncpg.exceptions.CannotConnectNowError):
        bot.logger.critical("Could not connect to psql.")
        
async def close_bot():
    await bot.wf.close()
    bot.logger.info("Closed Waifu Client")
    await bot.pool.close()
    bot.logger.info("Closed psql connection.")
    for task in asyncio.all_tasks(loop=bot.loop):
        task.cancel()
        bot.logger.info("Cancelled running task")
    await bot.session.close()
    bot.logger.info("Bot AIOHTTP client session closed")
    await bot.http.close()
    bot.logger.info("HTTP Session closed")
    await bot.close()
    bot.logger.info("logged out of bot")
    
try:
    bot.loop.run_until_complete(run_bot())
except KeyboardInterrupt:
    bot.loop.run_until_complete(close_bot())
        
bot.run(os.environ["TEST_TOKEN"])