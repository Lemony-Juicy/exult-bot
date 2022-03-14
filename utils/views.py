from discord import ButtonStyle, Interaction
from discord.ui import View, Button, Modal, TextInput
from numpy import place

from utils.tools import embed_builder

class Paginator(View):
    def __init__(self, pages, page=0, start_end=False, step_10=False):
        super().__init__(timeout=120)
        self.page = page
        self.pages = pages
        self.count = len(pages)
        self.start_end = start_end
        self.step_10 = step_10
        self.add_buttons()

    def add_buttons(self):
        non_page_buttons = [item for item in self.children if not isinstance(item, PaginatorButton)]
        if self.children:
            self.clear_items()
        if not self.count or self.count == 1:
            return
        previous_page = self.page - 1
        if previous_page < 0:
            previous_page = self.count - 1
        self.add_item(PaginatorButton(label="◀", page=previous_page, style=ButtonStyle.red))
        self.add_item(PaginatorButton(label=f"{self.page + 1} / {len(self.pages)}", style=ButtonStyle.grey, disabled=True))
        next_page = self.page + 1
        if next_page > self.count - 1:
            next_page = 0
        self.add_item(PaginatorButton(label="▶", page=next_page, style=ButtonStyle.green))
        for item in non_page_buttons:
            self.add_item(item)
            
class PaginatorButton(Button["Paginator"]):
    def __init__(self, label, style, row=0, page=None, disabled=False):
        super().__init__(style=style, label=label, row=row, disabled=disabled)
        self.page = page

    async def callback(self, interaction: Interaction):
        self.pages = self.view.pages
        self.view.page = self.page
        self.view.add_buttons()
        await interaction.message.edit(embed=self.pages[self.page], view=self.view)
        
class AvatarButton(Button):
    def __init__(self, label, style, custom_id):
        super().__init__(style=style, label=label, custom_id=custom_id)
        
    async def callback(self, interaction: Interaction):
        custom_id = interaction.data["custom_id"]
        member = await interaction.client.fetch_user(int(custom_id[6:]))
        await interaction.message.edit(embed=embed_builder(author=[member.display_avatar.url, f"{member.name}'s Avatar"],
                                                            image=member.display_avatar.url))

class BannerButton(Button):
    def __init__(self, label, style, custom_id):
        super().__init__(style=style, label=label, custom_id=custom_id)
        
    async def callback(self, interaction: Interaction):
        custom_id = interaction.data["custom_id"]
        member = await interaction.client.fetch_user(int(custom_id[6:]))
        await interaction.message.edit(embed=embed_builder(author=[member.display_avatar.url, f"{member.name}'s Banner"],
                                                            image=member.banner.url))
        
class Avatar(View):
    def __init__(self, member):
        super().__init__()
        self.add_item(AvatarButton("View Avatar", ButtonStyle.secondary, f"avatar{member.id}"))
        self.add_item(BannerButton("View Banner", ButtonStyle.secondary, f"banner{member.id}"))
        
class PokemonGuessModal(Modal):
    def __init__(self):
        self.guess = None
        super().__init__("Who's That Pokemon?")
        self.add_item(TextInput(label="Which pokemon do you think it is?", placeholder="e.g. Pikachu"))
        
    async def callback(self, interaction: Interaction):
        self.guess = self.children[0].value

class StartGuessPokemon(Button):
    def __init__(self, label, style, custom_id):
        super().__init__(style=style, label=label, custom_id=custom_id)
        
    async def callback(self, interaction: Interaction):
        modal = PokemonGuessModal()
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.view.guess = modal.guess

class PokemonGuess(View):
    def __init__(self, pokemon):
        self.guess = None
        super().__init__()
        self.add_item(StartGuessPokemon("Guess", ButtonStyle.blurple, pokemon))