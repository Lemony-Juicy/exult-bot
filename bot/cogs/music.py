import asyncio
from youtube_dl import YoutubeDL as ytdl
from youtubesearchpython import VideosSearch
import discord
import random
from discord.ext import commands
from bot.tools.organiser import badArg, convertSoup, makeBar, MenuChoose
from bot.tools.music import QueueState


def parseTime(t: str):
    if ':' not in t:
        return int(t)
    time_ = t.split(':')
    if len(time_) == 3:
        return int(time_[0]) * 3600 + int(time_[1]) * 60 + int(time_[2])
    return int(time_[0]) * 60 + int(time_[1])


def is_vc(both=False):
    async def predicate(ctx):
        voice = ctx.author.voice
        if voice is None:
            await ctx.send(embed=discord.Embed(description="You have to be in a voice channel to use this command",
                                               color=0x3400ff))
            return False
        return True if not both else ctx.voice_client is not None

    return commands.check(predicate)


def getYtLink(query, limit=1):
    videosSearch = VideosSearch(query, limit=limit)
    if not videosSearch.result():
        return
    info = []
    for r in videosSearch.result()["result"]:
        info.append([r["link"], r["title"], r["duration"]])
    return info


async def getUserSong(ctx, results):
    songs = []
    titles = list(map(lambda x: f"{x[1]}", results))
    large_titles = 0
    for i in range(0, len(titles)):
        if len(titles[i]) > 100:
            large_titles += 1
            titles[i] = i + 1
            songs.append(f'{i + 1}. {titles[i]}')
    description = '**`⚠️ These songs are not in the dropdown since their titles are too large. Please select the ' \
                  'number in the dropdown corresponding to the choices below if you would like to pick one of ' \
                  'these`**' + '\n'.join(songs)
    index = await MenuChoose(
        embed=discord.Embed(description=description if songs else '**`Select Songs from the dropdown below`**',
                            title='Options', color=0x2df755).set_footer(
            text="If you don't reply soon I will play the first option"), ctx=ctx).start(ctx, titles)
    return results[index]


ydl_opts = {
    'format': 'bestaudio/best',
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 50'
}


async def get_vc(ctx) -> discord.VoiceClient:
    vc = ctx.voice_client
    try:
        return await ctx.author.voice.channel.connect() if vc is None else vc
    except Exception as a:
        print(f"Error in get_vc(ctx): {a}")


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl(ydl_opts).extract_info(url=url, download=not stream))

        if 'entries' in data:  # if url is a playlist, take the first item
            data = data['entries'][0]

        filename = data['formats'][0]['url'] if stream else ytdl(ydl_opts).prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    """MAIN music commands in here. These commands include: playing, queueing and stopping/clearing music along with
    pausing, looping and resuming music. Newly added: NowPlaying command, fixed bug where music stops playing randomly."""

    def __init__(self, bot):
        self.bot = bot
        self.queue = QueueState()
        self.bot.loops = []

    def getVC(self, ctx: commands.Context):
        guild = discord.utils.get(self.bot.guilds, id=ctx.guild.id)  # type: discord.Guild
        return guild.voice_client

    def isLooped(self, server):
        return server in self.bot.loops

    async def play_queue(self, ctx):
        vc = await get_vc(ctx)
        if vc.is_playing():
            return
        q = self.queue.get(ctx)
        title, author, url = q['title'], q['author'], q['url']
        if self.getVC(ctx) is None:
            return
        embed = discord.Embed(description=f"**Playing** [{title}]({url}) **Now**\n[requested by "
                                          f"{author}]", color=0x00ffd9)
        player = await YTDLSource.from_url(url=url, loop=self.bot.loop, stream=True)
        song_message = await ctx.channel.send(embed=embed)
        vc.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(
            self.play_next(ctx, song_message, self.isLooped(ctx.guild.id)), self.bot.loop))
        self.queue.start_timer(ctx)

    async def play_next(self, ctx, song_message, loop):
        vc = self.getVC(ctx)
        if vc is None:
            return
        if not loop:
            self.queue.pull(ctx)
        if not self.queue.is_queue(ctx):
            self.queue.destroy_time(ctx)
            return
        q = self.queue.get(ctx)
        title, author, url = q['title'], q['author'], q['url']
        player = await YTDLSource.from_url(url=url, loop=self.bot.loop, stream=True)
        await song_message.delete()
        embed = discord.Embed(description=f"**Playing** [{title}]({url}) **Now**\n[requested by "
                                          f"{author}]", color=0x00ffd9)
        self.queue.destroy_time(ctx)
        song_message = await ctx.channel.send(embed=embed)
        vc.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(
            self.play_next(ctx, song_message, self.isLooped(ctx.guild.id)), self.bot.loop))
        self.queue.start_timer(ctx)

    @commands.command(aliases=['p'])
    @is_vc()
    async def play(self, ctx, *, query):
        """Play some music in voice chat! Specify a song to play"""
        async with ctx.typing():
            results = getYtLink(query, limit=10)
        if results is None:
            return await ctx.send(embed=discord.Embed(
                description="This is not a valid search query/it's too long, and I cannot play it\nOr this link/video"
                            " is age restricted", color=0xff0000))
        link, title, duration = await getUserSong(ctx, results)
        title_link = f"[{title}({duration})]({link})"
        self.queue.add_to_queue(ctx, title, link, ctx.author.mention, duration)
        await ctx.send(embed=discord.Embed(
            description=f"**Queued** [{title_link}]\n[requested by {ctx.author.mention}]",
            color=0x00ffc8))
        await self.play_queue(ctx)

    @commands.command(aliases=['qp', 'pq', 'playquick'])
    @is_vc()
    async def quickplay(self, ctx, *, query):
        """Play some music in voice chat! Specify a song to play"""
        async with ctx.typing():
            results = getYtLink(query)
        if results is None:
            return await ctx.send(embed=discord.Embed(
                description="This is not a valid search query/it's too long, and I cannot play it\nOr this link/video"
                            " is age restricted", color=0xff0000))
        link, title, duration = results[0]
        title_link = f"[{title}({duration})]({link})"
        self.queue.add_to_queue(ctx, title, link, ctx.author.mention, duration)
        await ctx.send(embed=discord.Embed(
            description=f"**Queued** [{title_link}]\n[requested by {ctx.author.mention}]",
            color=0x00ffc8))
        await self.play_queue(ctx)

    @commands.command()
    @is_vc()
    async def shuffle(self, ctx):
        """Shuffle the current queue"""
        if not self.queue.is_queue(ctx):
            return await ctx.send("The queue is empty, silly")
        self.queue.shuffle_queue(ctx)
        await ctx.send(embed=discord.Embed(description="I have shuffled thy queue, my lord", color=discord.Color.random()))

    @commands.command(aliases=['l'])
    @is_vc(True)
    async def loop(self, ctx):
        """Loop the current song playing"""
        if not self.isLooped(ctx.guild.id):
            self.bot.loops.append(ctx.guild.id)
            await ctx.send(embed=discord.Embed(description="🔄 Track is on looping 🔄", color=discord.Color.random()))
        else:
            self.bot.loops.remove(ctx.guild.id)
            await ctx.send(embed=discord.Embed(description="❗ Disabled looping track 🔄", color=0xff000c))

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        """View the current music queue"""
        if not self.queue.is_queue(ctx):
            return await ctx.reply(embed=discord.Embed(description="The current Queue is empty", color=0xff000c))
        await self.queue.display_queue(ctx, self.bot)

    @commands.command(aliases=['nowPlaying', 'nowPlay'])
    async def np(self, ctx):
        if ctx.guild.id not in self.queue.timer or ctx.voice_client is None:
            return await ctx.send("Nothing is currently playing")
        if ctx.guild.id in self.queue.timer and ctx.voice_client is not None:
            n = self.queue.get(ctx)
            time = self.queue.get_time(ctx)
            total = parseTime(self.queue.get(ctx)['duration'])
            bar = makeBar(time, total, length=25, start='[', fill='-', noFill='-', end='⨷', last=']')
            return await ctx.send(embed=discord.Embed(
                description=f"Currently playing [{n['title']}]({n['url']})\n{bar}\n`{self.queue.get_time(ctx)}/"
                            f"{parseTime(self.queue.get(ctx)['duration'])}s`", color=discord.Color.random()))

    @commands.command(aliases=['rq'])
    @is_vc(True)
    async def remove(self, ctx, index: int):
        """Remove a song from the queue by specifying the order the number of that song. To see this view {queue}"""
        if not self.queue.is_queue(ctx):
            return await ctx.reply(embed=discord.Embed(description="The current Queue is empty", color=0xff000c))
        index -= 1
        if index == 0:
            return await ctx.send(f"To remove current track do [skip]")
        try:
            title_link = self.queue.pull(ctx, index)
            await ctx.send(
                embed=discord.Embed(description=f"Removed {title_link} from queue."
                                                f"\n[removed by {ctx.author.mention}]", color=0x00ffcd))
        except IndexError:
            await ctx.send(
                f"❌You Have to provide a valid list number to remove from the queue list❌ Use [queue/q] "
                "for the queue list")

    @remove.error
    async def removeError(self, ctx, error):
        await badArg(ctx, error,
                     f"You have to provide a list number for the queue list to be removed. See [queue/q] for the current"
                     "queue")

    @commands.command()
    @is_vc()
    async def music(self, ctx):
        """Play random music. This also adds it to the queue if other music if playing before it"""
        async with ctx.typing():
            soup = convertSoup('https://www.bestrandoms.com/random-song-generator')
            song = soup.find(class_='content').find('img')['alt']
            link, title, duration = getYtLink(song, limit=5)[random.randint(0, 4)]
            title_link = f"[{title}]({link}) `duration: {duration}`"
        self.queue.add_to_queue(ctx, title, link, ctx.author.mention,
                                duration)
        await ctx.send(embed=discord.Embed(
            description=f"Queued [{title_link})\n[Random music requested by {ctx.author.mention}]",
            color=discord.Color.random()))
        await self.play_queue(ctx)

    @commands.command()
    @is_vc(True)
    async def stop(self, ctx):
        """Stop and clear the queue. use {pause} to pause the current song"""
        vc = await get_vc(ctx)
        if not self.queue.is_queue(ctx):
            return await ctx.reply(embed=discord.Embed(description="The current Queue is empty"))
        async with ctx.typing():
            self.queue.delete(ctx)
            vc.stop()
        await ctx.send(
            embed=discord.Embed(description=f"Stopped and cleared queue ting\n[{ctx.author.mention}]", color=0x00ffcc))
        self.queue.destroy_time(ctx)

    @commands.command()
    @is_vc(True)
    async def skip(self, ctx):
        """Skip the current song playing"""
        vc = await get_vc(ctx)  # type: discord.VoiceClient
        if not self.queue.is_queue(ctx):
            return await ctx.reply(embed=discord.Embed(description="The current Queue is empty", color=0xff000c))
        async with ctx.typing():
            if ctx.guild.id in self.bot.loops:
                self.bot.loops.remove(ctx.guild.id)
                vc.stop()
                self.bot.loops.append(ctx.guild.id)
            else:
                vc.stop()
        await ctx.send(
            embed=discord.Embed(description=f"Skipped Current Track\n[{ctx.author.mention}]", color=0x00ffcc))

    @commands.command()
    @is_vc(True)
    async def pause(self, ctx):
        """Pause the current song that is playing"""
        vc = await get_vc(ctx)  # type: discord.VoiceClient
        if not self.queue.is_queue(ctx) or vc.is_paused():
            return await ctx.send(
                f"You can only use this cmd when I am playing something and you want to pause it. use [resume]"
                "to resume")
        vc.pause()
        self.queue.pause_timer(ctx)
        return await ctx.send("✅ paused track ✅")

    @commands.command()
    @is_vc(True)
    async def resume(self, ctx):
        """If the song is paused, use this to resume it"""
        vc = await get_vc(ctx)
        if not self.queue.is_queue(ctx) or not vc.is_paused():
            return await ctx.send(
                f"You can only use this cmd when I have paused a track and you want to resume it. use [pause]"
                "to pause track when playing")
        try:
            vc.resume()
        except Exception as a:
            await ctx.send(f"I can't do this - {a}")
        self.queue.resume_timer(ctx)
        return await ctx.send("✅ resumed track ✅")

    @commands.command()
    @is_vc()
    async def join(self, ctx):
        """Make me join the voice chat that you're in"""
        try:
            vc = await ctx.author.voice.channel.connect()
            vc.resume()
            if self.queue.is_queue(ctx) and not (await get_vc(ctx)).is_playing():
                q = self.queue.get(ctx)
                title, author, url = q['title'], q['author'], q['url']
                embed = discord.Embed(description=f"**Playing** [{title}]({url}) **Now**\n[requested by "
                                                  f"{author}]", color=0x00ffd9)
                player = await YTDLSource.from_url(url, loop=self.bot.loops, stream=True)
                song_message = await ctx.send(embed=embed)
                vc.play(player, after=lambda p: asyncio.run_coroutine_threadsafe(self.play_next(ctx, song_message,
                                                                                                self.isLooped(
                                                                                                    ctx.guild.id)),
                                                                                 self.bot.loop))
                self.queue.start_timer(ctx)
                await ctx.message.add_reaction("👍")
        except Exception as e:
            print(e)
            await ctx.message.add_reaction("❌")

    @commands.command(aliases=['ds', 'leave', 'dc'])
    @is_vc(True)
    async def disconnect(self, ctx):
        """Disconnect me from vc"""
        vc = ctx.voice_client
        if vc is None:
            return await ctx.send(embed=discord.Embed(description="I cannot do this", color=0xff0000))
        await vc.disconnect()
        await ctx.send(embed=discord.Embed(description=f"Goodbye {ctx.author.mention}", color=0x00ffcc))

    async def leaveIfEmpty(self, before, guild):
        vc = guild.voice_client
        if len(before.members) == 1:
            await asyncio.sleep(100)
            members = list(map(lambda x: x.id, self.bot.get_channel(vc.channel.id).members))
            if self.bot.user.id in members and len(members) == 1:
                guild.voice_client.pause()
                await guild.voice_client.disconnect()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after):
        guild = member.guild  # type: discord.Guild

        # If person left the channel the bot was in:
        if not after.channel and guild.voice_client and before.channel and before.channel == guild.voice_client.channel:
            await self.leaveIfEmpty(before.channel, guild)

        if after.channel and before.channel and after.channel != before.channel:
            if guild.voice_client is not None:
                guild.voice_client.resume()


def setup(bot):
    bot.add_cog(Music(bot))
