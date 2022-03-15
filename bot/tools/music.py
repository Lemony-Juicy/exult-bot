from bot.tools.organiser import get_chunks, Paginator
import time
from discord.ext import commands
import discord
import random


class QueueState:
    def __init__(self):
        self.queue = {}
        self.timer = {}
        self.pause_elapsed = {}
        self.pause_start = {}

    def start_timer(self, ctx):
        self.timer[ctx.guild.id] = time.time()

    def get_time(self, ctx):
        elapsedTime = time.time() - self.timer[ctx.guild.id]
        if ctx.guild.id in self.pause_start:
            elapsedTime -= self.paused_time(ctx)
        return round(elapsedTime)

    def pause_timer(self, ctx):
        self.pause_start[ctx.guild.id] = [time.time(), False]  # second index: False = not unPaused, True = unPaused

    def resume_timer(self, ctx):
        if ctx.guild.id in self.pause_elapsed:
            self.pause_elapsed[ctx.guild.id] += time.time() - self.pause_start[ctx.guild.id][0]
        else:
            self.pause_elapsed[ctx.guild.id] = time.time() - self.pause_start[ctx.guild.id][0]
        self.pause_start[ctx.guild.id][1] = True

    def paused_time(self, ctx):
        if ctx.guild.id in self.pause_elapsed:
            if not self.pause_start[ctx.guild.id][1]:
                return self.pause_elapsed[ctx.guild.id] + (time.time() - self.pause_start[ctx.guild.id][0])
            return self.pause_elapsed[ctx.guild.id]
        return time.time() - self.pause_start[ctx.guild.id][0]

    def destroy_time(self, ctx):
        if ctx.guild.id in self.pause_elapsed:
            del self.pause_elapsed[ctx.guild.id]
            del self.pause_start[ctx.guild.id]
        del self.timer[ctx.guild.id]

    def add_to_queue(self, ctx: commands.Context, title, url, author, duration: str):
        if ctx.guild.id not in self.queue:
            self.queue[ctx.guild.id] = [
                {'author': author, 'title': title, 'url': url, 'duration': duration}]
            return
        self.queue[ctx.guild.id].append(
            {'author': author, 'title': title, 'url': url, 'duration': duration})

    def is_queue(self, ctx: commands.Context, one=False):
        if one:
            return len(self.queue[ctx.guild.id]) == 1
        return self.queue.get(ctx.guild.id) if self.queue.get(ctx.guild.id) is not None else False

    async def display_queue(self, ctx: commands.Context, bot):
        if self.is_queue(ctx) is None:
            return await ctx.reply(embed=discord.Embed(description="The current Queue is empty", color=0xff000d))
        queue_songs = []
        song_counter = 1
        async with ctx.typing():
            for s in self.queue[ctx.guild.id]:
                queue_songs.append(f"`{song_counter}. ({s['duration']})` {s['author']} [{s['title']}]({s['url']})")
                song_counter += 1
        pages = get_chunks(10, queue_songs)
        if len(pages) == 1:
            embed = discord.Embed(description='\n'.join(queue_songs), title="Current Playlist", color=0x00fcf0)
            return await ctx.reply(embed=embed)
        embeds = []
        for i in range(len(pages)):
            embeds.append(discord.Embed(description='\n'.join(pages[i]), title=f"Page {i+1}", color=0x00fcf0))
        await Paginator(embeds, ctx).start()

    def get(self, ctx):
        return self.queue[ctx.guild.id][0]

    def pull(self, ctx: commands.Context, index=0):
        this = self.queue[ctx.guild.id][index]
        self.queue[ctx.guild.id].pop(index)
        return f"[{this['title']}]({this['url']})"

    def delete(self, ctx: commands.Context):
        del self.queue[ctx.guild.id]

    def shuffle_queue(self, ctx):
        try:
            current = self.get(ctx)
            self.queue[ctx.guild.id] = self.queue[ctx.guild.id][1:]
            random.shuffle(self.queue[ctx.guild.id])
            self.queue[ctx.guild.id].insert(0, current)
        except IndexError:
            return
