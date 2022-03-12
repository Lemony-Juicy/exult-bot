import discord
from discord import app_commands
from discord.ext.commands import Bot, Cog, command, Context

class TestCog(Cog): #Normal Cog containing commands and listeners
    def __init__(self, bot: Bot):
        self.bot = bot
        
    @command()
    async def test(self, ctx: Context):
        await ctx.send("Test Successful!")
        
class TestModal(discord.ui.Modal, title="Modal which is a test one"):
    default = discord.ui.TextInput(label="Name")
    short = discord.ui.TextInput(label="Name", style=discord.TextStyle.short)
    paragraph = discord.ui.TextInput(label="Answer", style=discord.TextStyle.paragraph)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Thanks for your response of {self.default}!", ephemeral=True)
        
@app_commands.command(description="Test slash command")
async def slash_test(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hey, {name}!", ephemeral=True)
    
@app_commands.command()
async def modal_slash_test(interaction: discord.Interaction):
    await interaction.response.send_modal(TestModal())
        
@app_commands.context_menu()
async def bonk(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message('Bonk', ephemeral=True)

@app_commands.command(name="rangeoption", description="Slash command with range defined for param")
async def range_option(interaction: discord.Interaction, value: app_commands.Range[int, 1, 100]):
    await interaction.response.send_message(f"You selected number {value}", ephemeral=True)

@app_commands.command()
async def fruits(interaction: discord.Interaction, fruit: str):
    await interaction.response.send_message(f'Your favourite fruit seems to be {fruit}')

@fruits.autocomplete('fruit')
async def fruits_autocomplete(interaction: discord.Interaction, current: str, namespace: app_commands.Namespace):
    fruits = ['Banana', 'Pineapple', 'Apple', 'Watermelon', 'Melon', 'Cherry']
    return [app_commands.Choice(name=fruit, value=fruit) for fruit in fruits if current.lower() in fruit.lower()]
        
def setup(bot: Bot):
    bot.add_cog(TestCog(bot))
    tree: app_commands.CommandTree = bot.tree
    tree.add_command(slash_test, guild=discord.Object(id=912148314223415316))
    tree.add_command(modal_slash_test, guild=discord.Object(id=912148314223415316))
    tree.add_command(bonk, guild=discord.Object(id=912148314223415316))
    tree.add_command(range_option, guild=discord.Object(id=912148314223415316))
    tree.add_command(fruits, guild=discord.Object(id=912148314223415316))