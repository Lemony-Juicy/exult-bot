import discord

from discord.ext import commands

from math import *
from database.leveling import LevelingDB

from easy_pil import Canvas, Editor, Font
import os


EXP_PER_MESSAGE = 20

# Exult's Formula by Ethan
# reference: https://i.imgur.com/LA0JLty.png
def exults_formula(lvl) -> int:
    return round((pi**-(e**(1/factorial(3)*gamma(pi))/10))*(log(e**(lvl*2)**1.078)*cosh(pi))*10/100)*100


class LevelingDbClient:
    def __init__(self, bot):
        self.bot = bot
    
    async def add_xp(self, user, ctx):
        if ctx.guild.id == 912148314223415316:
            x = LevelingDB(self.bot.db)
            res = await x.add_xp(user.id, EXP_PER_MESSAGE, user.guild.id)
            if res in [[], None]:
                return

            if int(res[0][0]) >= exults_formula(int(res[0][1])):
                await x.levelup(user.id, user.guild, int(res[0][0]) - exults_formula(int(res[0][1])))
                
                try:
                    msg = await x.get_custom_message(ctx.guild.id)
                except:
                    msg = f"{user.name} has leveled up to level {res[0][1]}!"
                else:
                    if msg is None:
                        msg = f"{user.name} has leveled up to level {res[0][1]}!"
                    else:
                        msg = msg[0][0]
                try:
                    channel = await x.get_custom_channel(ctx.guild.id)
                except:
                    channel = None

                if channel:
                    channel = self.bot.get_channel(int(channel[0][0]))
                    return await channel.send(msg)
                
                await ctx.channel.send(msg)



class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = LevelingDbClient(bot)
        self.db = LevelingDB(bot.db)
    
    # setbio command
    @commands.command(aliases=["sb"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def setbio(self, ctx, *, msg: str = None):
        if ctx.guild.id == 912148314223415316:
            if not msg:
                return await ctx.send("Please provide a message to set as your bio.")
            
            await self.db.set_bio(ctx.author.id, msg)

            await ctx.send("Done! Your bio has been set to {}.".format(msg))

    @commands.command(aliases=["lvl", "level", "xp", "exp", "stats"], description="Lookup someone's stats on the server")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rank(self, ctx, member: discord.Member = None):
        """ Lookup someone's stats on the server """
        if ctx.guild.id == 912148314223415316:
            member = ctx.author if not member else member
            xp = await self.db.get_xp(member.id, ctx.guild.id)
            xp = str(xp[0][0])
            lvl = await self.db.get_level(member.id, ctx.guild.id)
            lvl = str(lvl[0][0])
            if xp == "0":
                percentage = 0
            else:
                percentage = round(int(xp)/exults_formula(int(lvl))*100)
            
            bio = await self.db.get_bio(member.id)

            user_data = {
                "name": f"{member.name}#{member.discriminator}",
                "bio": str(bio[0][0]) if bio[0][0] else f"No bio set. Set one using setbio (premium-only feature)",
                "level": lvl,
                "xp":  xp,
                "xp2": exults_formula(int(lvl)),
                "percentage": percentage,
            }
            # get the users avatar and save it as a png file

            background = Editor(Canvas((934, 282), "#352a2a"))
            try:
                profile = Editor(f"assets/{member.name}_pfp.png").resize((200, 200)).circle_image()
            except:
                await member.avatar.save(f"assets/{member.name}_pfp.png")
                profile = Editor(f"./assets/{member.name}_pfp.png").resize((200, 200)).circle_image()

            background = Editor(Canvas((800, 240), color="#23272A"))

            # For profile to use users profile picture load it from url using the load_image/load_image_async function
            # profile_image = load_image(str(ctx.author.avatar_url))
            # profile = Editor(profile_image).resize((200, 200))


            font_40 = Font.poppins(size=40)
            font_20 = Font.montserrat(size=20)
            font_25 = Font.poppins(size=25)
            font_40_bold = Font.poppins(size=40, variant="bold")

            background.paste(profile, (20, 20))
            background.text((240, 20), user_data["name"], font=font_40, color="white")
            background.text((240, 80), user_data["bio"], font=font_20, color="white")
            background.text((250, 170), "LVL", font=font_25, color="white")
            background.text((310, 155), user_data["level"], font=font_40_bold, color="white")

            background.rectangle((390, 170), 360, 25, outline="white", stroke_width=2)
            background.bar(
                (394, 174),
                352,
                17,
                percentage=user_data["percentage"],
                fill="white",
                stroke_width=2,
            )

            background.text((390, 135), "Rank : 0", font=font_25, color="white")
            background.text(
                (750, 135), f"XP : {user_data['xp']}/{user_data['xp2']}", font=font_25, color="white", align="right"
            )
            file = discord.File(fp=background.image_bytes, filename=f"{member.name}_rank.png")
            await ctx.send(file=file)

            os.remove(f"assets/{member.name}_pfp.png")

    @commands.group(aliases=["lvls", "levels"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def levelling(self, ctx):
        pass
    
    @levelling.command(description="Turn on levelling for the server")
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def on(self, ctx):
        await self.db.set_levelling(ctx.guild.id, True)
        await ctx.send(f"{ctx.author.mention} has turned on levelling for the server!")
    
    @levelling.command(description="Turn off levelling for the server")
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def off(self, ctx):
        await self.db.set_levelling(ctx.guild.id, False)
        await ctx.send(f"{ctx.author.mention} has turned off levelling for the server!")

    @levelling.command(description="Turn off levelling for the server")
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def toggle(self, ctx):
        res = await self.db.set_levelling(ctx.guild.id, None)
        await ctx.send(f"{ctx.author.mention} has turned {'on' if res else 'off'} levelling for the server!")
    
    @commands.command(description="Displays the top-10 users with the highest level", aliases=['lb', 'leaderboard'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def top(self, ctx):
        res = await self.db.leaderboard(ctx.guild.id)

        if not res:
            return await ctx.send("No one has leveled up yet!")
        
        embed = discord.Embed(title="Top 10 Users", description="", color=self.bot.red)
        
        # iterate through the results and add them to the embed
        for i, r in enumerate(res):
            user = ctx.guild.get_member(r[0])
            embed.description += f"**{i+1}.** {user.name}#{user.discriminator}: **Level:** {r[2]}\n"

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Leveling(bot))
