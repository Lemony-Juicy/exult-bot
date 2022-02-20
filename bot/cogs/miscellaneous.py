import discord
from discord.ext import commands
import kimetsu
Embed = kimetsu.embed.Embed.embed

import random
from psutil import Process, cpu_percent
from os import getpid

e_arrow = "<a:arrow:882812954314154045>"

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member: discord.Member=None):
        """Show the avatar of the mentioned member"""
        await kimetsu.Avatar(ctx, member).avatar()
        
    @commands.command(aliases=['ri'])
    async def roleinfo(self, ctx, role: discord.Role):
        """Display info on a specified role"""
        await kimetsu.Roleinfo(ctx, role).roleinfo()
            
    @commands.command(aliases=['si'])
    async def serverinfo(self, ctx):
        """Display info on the server you're currently in"""
        await kimetsu.Serverinfo(ctx).serverinfo()
        
    @commands.command(aliases=['rolememberinfo', 'rmi', 'ir'])
    async def inrole(self, ctx, *, role: discord.Role):
        """Display every member who has a specified role"""
        await kimetsu.Inrole(ctx, role).inrole()
        
    @commands.command(aliases=['ui', 'whois'])
    async def userinfo(self, ctx, member: discord.Member=None):
        """Displays info on the mentioned member"""
        await kimetsu.Userinfo(ctx, member).userinfo()
        
    @commands.command(description="Pong! 🏓")
    async def ping(self, ctx):
        """Pong! 🏓"""
        await ctx.send(f"Pong! 🏓\n**Latency:** `{round(self.bot.latency*1000)}ms`\n**PSQL Latency:** `{round(await self.bot.get_latency()*1000, 2)}ms`")

    @commands.command(description="invite the bot to your server!")
    async def invite(self, ctx):
        """Invite the bot to your server"""
        await ctx.send(embed=Embed(title="Click to invite me!", url=self.bot.invite, timestamp=True))

    @commands.command(description="join our support server!")
    async def support(self, ctx):
        """Get an invite to our support server"""
        await ctx.send(embed=Embed(title="Click to join the support server!", url="https://discord.gg/NAFTAtAz5d", timestamp=True))

    @commands.command()
    async def rng(self, ctx, limit: int):
        """Generate a random number between 1 and the number you provide"""
        num = random.randint(1, limit)
        await ctx.message.reply(embed=discord.Embed(title=f"Your random number is {num}!", colour=discord.Colour.green()))

    @commands.command(description="displays bot information")
    async def info(self, ctx):
        """Send bot information."""
        msg = f"""**Bot version:** `{self.bot.__version__}`
**Database Version:** `{self.bot.db.__version__}`
**Edpy version:** `{discord.__version__}`
**Guild Count:** `{len(self.bot.guilds)}`
**Memory Used:** `{round(Process(getpid()).memory_info().rss/1204/1204/1204, 3)}GB Used ({round(Process(getpid()).memory_percent())}%)`
**CPU Usage:** `{cpu_percent()}%`
**Creators:** `Andeh#2709`, `Erase#0027`
"""

        embed = Embed(
            title="Bot information",
            description=msg,
            thumb=str(self.bot.user.avatar),
            timestamp=True,

        )

        await ctx.send(embed=embed)

    @commands.command(description="send feedback to the developer server")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def feedback(self, ctx, *, message=None):
        """Send feedback to the developer server"""
        if message is None:
            return await ctx.send("Please specify a message!")
        
        channel = await self.bot.fetch_channel(914193452428836884)
        
        embed = Embed(
            title=f"Feedback from {ctx.author.name}#{ctx.author.discriminator}",
            description=message,
            timestamp=True
        )
        
        msg = await channel.send(embed=embed)
        
        await ctx.send("Message sent! Thanks for your feedback!")
        
    @commands.command()
    @commands.has_permissions(change_nickname=True)
    async def nick(self, ctx, nick: str):
        """Edit your own nickname!"""
        await ctx.author.edit(nick=nick)
        await ctx.send(embed=discord.Embed(description=f"Changed {ctx.author}'s nickname to {nick}", colour=self.bot.red))
        
def setup(bot):
    bot.add_cog(Miscellaneous(bot))