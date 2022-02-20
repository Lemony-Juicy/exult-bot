import discord
from discord import SlashCommand
from discord.ext import commands

from ..modal import Modal
        
class SlashTest(SlashCommand, name="testslash", guilds=[912148314223415316]):
    
    async def callback(self) -> None:
        modal = Modal()
        await self.interaction.response.send_modal(modal)
        
class SlashTest2(SlashCommand, name="testslash2", guilds=[912148314223415316]):
    name: str = discord.app.Option(description="What is your name?")
    async def callback(self) -> None:
        await self.interaction.response.send_message(content=f"Hello, {self.name}!", ephemeral=True)
        
class SlashTest3(SlashCommand, name="testslash3", guilds=[912148314223415316], description="Tell me a bit about yourself!"):
    name: str = discord.app.Option(description="What is your name?")
    age: int = discord.app.Option(description="How old are you?", autocomplete=True)
    
    async def autocomplete(self, options, focused):
        choices = {"13": 13, "14": 14, "15": 15, "16": 16, "17": 17, "18": 18}
        return discord.app.AutoCompleteResponse(choices)
    
    async def callback(self) -> None:
        await self.interaction.response.send_message(content=f"Hello, {self.name} who is {self.age} years old!!", ephemeral=True)
                
def setup(bot):
    bot.application_command(SlashTest)
    bot.application_command(SlashTest2)
    bot.application_command(SlashTest3)
