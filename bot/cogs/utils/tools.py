import discord
import re
from datetime import datetime, timedelta
from typing import Union

class Time:
    def handler(time):
        secsearch = re.search("s?ec|s", time)
        minsearch = re.search("m?in|m", time)
        hoursearch = re.search("h?our|h", time)
        daysearch = re.search("d?ay|d", time)
        nums = re.findall("\d", time)
        num = "".join(nums)

        if secsearch:
            dtype = "seconds"
        if minsearch:
            dtype = "minutes"
        if hoursearch:
            dtype = "hours"
        if daysearch:
            dtype = "days"
        if int(num) == 1:
            dtype = dtype[:-1]
        return [num, dtype]

    def parsedate(date=None):
        date = datetime.now() if date is None else date
        timestamp = datetime.timestamp(date)
        timestamp = str(timestamp).split('.', 1)[0]
        return f"<t:{timestamp}:F>"

    def formatdate(date=None):
        print(date)
        date = datetime.now() if date is None else date
        return date.strftime("%d/%m/%Y %H:%M")

    def convert_for_command(time: Union[datetime, list]):
        if isinstance(time, list):
            num = int(time[0])
            ttype = str(time[1])
            if ttype.startswith("s"):  
                return datetime.utcnow() + timedelta(seconds=num)
            elif ttype.startswith("mi"):
                return datetime.utcnow() + timedelta(minutes=num)
            elif ttype.startswith("h"):
                return datetime.utcnow() + timedelta(hours=num)
            elif ttype.startswith("d"):
                return datetime.utcnow() + timedelta(days=num)
        elif isinstance(time, datetime):
            return datetime.utcnow() + time

class Embed:
    def __init__(self, bot):
        self.bot = bot

    def embed(self, *, title=None, description=None, colour=None, thumbnail=None, image=None, author: Union[dict, None]=None, footer: Union[dict, None]=None, timestamp: Union[datetime, None]=None):
        e = discord.Embed(title="" if not title else title, 
                          description="" if not description else description, 
                          colour=self.bot.red if not colour else colour,
                          timestamp=None if not timestamp else timestamp)
        if thumbnail:
            e.set_thumbnail(url=thumbnail)
        if image:
            e.set_image(url=image)
        if author:
            e.set_author(icon_url=author["icon"], name=author["name"])
        if footer:
            e.set_footer(icon_url=footer["icon"], text=footer["text"])
        return e
        