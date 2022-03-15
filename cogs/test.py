
from discord import app_commands, TextStyle, Interaction, Object, Member
from discord.ui import TextInput, Modal
        
class TestModal(Modal, title="Modal which is a test one"):
    default = TextInput(label="Name")
    short = TextInput(label="Name", style=TextStyle.short)
    paragraph = TextInput(label="Answer", style=TextStyle.paragraph)
    
    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message(f"Thanks for your response of {self.default}!", ephemeral=True)
        
@app_commands.command(description="Test slash command")
async def slash_test(interaction: Interaction, name: str):
    await interaction.response.send_message(f"Hey, {name}!", ephemeral=True)
    
@app_commands.command()
async def modal_slash_test(interaction: Interaction):
    await interaction.response.send_modal(TestModal())
        
@app_commands.context_menu()
async def bonk(interaction: Interaction, member: Member):
    await interaction.response.send_message('Bonk', ephemeral=True)

@app_commands.command(name="rangeoption", description="Slash command with range defined for param")
async def range_option(interaction: Interaction, value: app_commands.Range[int, 1, 100]):
    await interaction.response.send_message(f"You selected number {value}", ephemeral=True)

@app_commands.command()
async def fruits(interaction: Interaction, fruit: str):
    await interaction.response.send_message(f'Your favourite fruit seems to be {fruit}')

@fruits.autocomplete('fruit')
async def fruits_autocomplete(interaction: Interaction, current: str, namespace: app_commands.Namespace):
    fruits = ['Banana', 'Pineapple', 'Apple', 'Watermelon', 'Melon', 'Cherry']
    return [app_commands.Choice(name=fruit, value=fruit) for fruit in fruits if current.lower() in fruit.lower()]
        
async def setup(bot):
    commands = [slash_test, modal_slash_test, bonk, range_option, fruits]
    guilds = [912148314223415316, 949429956843290724]
    for command in commands:
        bot.tree.add_command(command, guilds=[Object(guild) for guild in guilds])
        print(f"Added {command.name} to {guilds}")