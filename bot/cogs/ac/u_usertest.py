import discord
from discord import UserCommand
import kimetsu
from cogs.utils.tools import Embed

class AvatarUserCommand(UserCommand, name="avatar"):
    async def callback(self):
        user = self.target
        embed = discord.Embed(title=f"{user}'s Avatar", colour=0xfb5f5f).set_image(url=user.display_avatar.url).set_footer(icon_url=self.interaction.user.display_avatar.url, text=f"Requested by: {self.interaction.user}")
        await self.interaction.response.send_message(embed=embed)
    
def setup(bot):
    bot.application_command(AvatarUserCommand)
