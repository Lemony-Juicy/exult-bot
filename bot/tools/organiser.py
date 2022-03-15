import discord
from discord.ext import commands
import asyncio
from bs4 import BeautifulSoup
import requests
red = 0xff0000
green = 0x00ff00
HEADER = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, '
                        'like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53.'}


def convertSoup(link, user_agent=None):
    if user_agent is None:
        user_agent = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, '
                          'like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53.'}
    if user_agent is not None:
        return BeautifulSoup(requests.get(link, headers=user_agent, timeout=5).content, 'html.parser')
    page = requests.get(link, timeout=5)
    return BeautifulSoup(page.content, 'html.parser')


def get_chunks(interval: int, array: list):
    """split up an array into a two-dimensional array with the interval specified"""
    total = []
    a = 0
    if len(array) <= interval:
        return [array]
    for i in range(len(array) // interval):
        chunks = []
        for _ in range(interval):
            chunks.append(array[a])
            a += 1
        total.append(chunks)
    if len(array) % interval != 0:
        total.append(array[a:])
    return total


def makeBar(val1, val2, length=18, start='', end='', fill='▰', noFill='▱', last=''):
    bar = ''
    normalise = val1 / val2 if val2 >= val1 else val2 / val1
    progress = round(normalise * length)
    rest_of_bar = round(length - progress) if length >= progress else 0
    for i in range(progress):
        bar += fill
    bar += end
    for i in range(rest_of_bar):
        bar += noFill
    bar += last
    return start + bar


async def badArg(ctx, error, desc):
    if isinstance(error, commands.MissingRequiredArgument):
        msg = discord.Embed(description=desc, color=red)
        msg.set_footer(text="❌ Missing Required Argument ❌\nYou need a second argument.")
        await ctx.send(embed=msg)
    elif isinstance(error, commands.BadArgument):
        msg = discord.Embed(description=desc, color=red)
        msg.set_footer(text="❌ Bad Argument(s) ❌")
        await ctx.send(embed=msg)


class Paginator(discord.ui.View):
    def __init__(self, embeds: [discord.Embed], ctx: commands.Context, time_out=30, reply=False):
        super().__init__(timeout=time_out)
        self.embeds = embeds
        self.size = len(embeds)
        self.index = 0
        self.pages.label = f"{self.index + 1}/{self.size}"
        self.ctx = ctx
        self.message = None
        self.reply = reply

    async def on_timeout(self) -> None:
        self.previous.disabled = True
        self.next.disabled = True
        await self.message.edit(view=self)

    async def start(self) -> None:
        if self.reply:
            self.message = await self.ctx.reply(embed=self.embeds[self.index], view=self)
        else:
            self.message = await self.ctx.send(embed=self.embeds[self.index], view=self)

    def increment_index(self):
        self.index = (self.index + 1) % self.size

    def decrement_index(self):
        self.index = (self.index - 1) % self.size

    @discord.ui.button(label="⬅", style=discord.ButtonStyle.blurple)
    async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.decrement_index()
        self.pages.label = f"{self.index + 1}/{self.size}"
        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)

    @discord.ui.button(label="", style=discord.ButtonStyle.grey, disabled=True)
    async def pages(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label="➡", style=discord.ButtonStyle.blurple)
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.increment_index()
        self.pages.label = f"{self.index + 1}/{self.size}"
        await interaction.response.edit_message(embed=self.embeds[self.index], view=self)


class MenuChoose(discord.ui.View):
    """Create menu options by initiating the class with the send kwargs (including timeout), and then begin the
    MenuChoose by 'start' method. Provide the array of SelectOption labels"""

    def __init__(self, **kwargs):
        super().__init__(timeout=35 if kwargs.get('timeout') is None else kwargs['timeout'])
        if 'timeout' in kwargs:
            del kwargs['timeout']
        self.ctx = kwargs['ctx']
        del kwargs['ctx']
        self.kwargs = kwargs
        self.message = None
        self.has_chose = False
        self.index = 0

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message("This message isn't for you, silly", ephemeral=True)
        print(interaction.data)
        value = interaction.data['values'][0]
        self.index = int(value)
        await self.message.delete()
        self.has_chose = True

    async def on_timeout(self) -> None:
        await self.message.delete()
        self.has_chose = True

    async def start(self, ctx, array: list, placeholder="Select a song", returnNone=False):
        options = []
        self.index = None if returnNone else 0
        for i in enumerate(array):
            options.append(discord.SelectOption(label=i[1], value=str(i[0])))
        drop_down = discord.ui.Select(options=options, placeholder=placeholder)
        drop_down.callback = self.callback
        self.add_item(drop_down)
        self.message = await ctx.send(**self.kwargs, view=self)
        while not self.has_chose:
            await asyncio.sleep(1)
        return self.index
