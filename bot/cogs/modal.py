import discord
from discord.ext import commands
from discord.ui import Modal, TextInput, View

class Modal(Modal):
    def __init__(self):
        super().__init__("Test Modal")
        self.add_item(TextInput(label="What is your name?", placeholder="Enter your name..."))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {self.children[0].value}", ephemeral=True)

class ModalView(View):
    @discord.ui.button(label="Open Modal", style=discord.ButtonStyle.green)
    async def open_modal(self, button: discord.Button, interaction: discord.Interaction):
        modal = Modal()
        await interaction.response.send_modal(modal)

class ModalTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testmodal(self, ctx):
        view = ModalView()
        await ctx.message.reply("Here's the modal lul", view=view)

def setup(bot):
    bot.add_cog(ModalTest(bot))