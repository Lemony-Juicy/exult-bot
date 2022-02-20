from cProfile import label
import discord
from ast import literal_eval

from database.suggestions import SuggestDB
    
class CategoriesDropdown(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.ctx.guild.categories]
        super().__init__(placeholder="Select a Category", options=options, min_values=1, max_values=1)
        
    async def callback(self, interaction: discord.Interaction):
        self.view.values = self.values
        self.view.stop()

class CategoriesDropdownView(discord.ui.View):
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__()
        self.add_item(CategoriesDropdown(self.ctx))

    
class ChannelsDropdown(discord.ui.Select):
    def __init__(self, cat):
        self.cat = cat
        options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.cat.text_channels]
        super().__init__(placeholder="Select a Channel", options=options, min_values=1, max_values=1)
        
    async def callback(self, interaction: discord.Interaction):
        self.view.values = self.values
        self.view.stop()
        
class ChannelsDropdownView(discord.ui.View):
    def __init__(self, cat):
        self.cat = cat
        super().__init__()
        self.add_item(ChannelsDropdown(self.cat))

            
class ConfirmDenyView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        
    @discord.ui.button(label="✅", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()
        
    @discord.ui.button(label="❌", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        self.stop()


class OpenTicket(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji="📥", custom_id="OpenTicket")
    async def openticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        return

class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="❌", custom_id="CloseTicket")
    async def closeticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        return


class SuggestConfEditMain(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        options = [discord.SelectOption(label="Edit Suggestions Channel", value="Suggestions Channel"), discord.SelectOption(label="Edit Safemode", value="Safemode"), discord.SelectOption(label="Disable Feature", value="Disable")]
        super().__init__(placeholder="What setting would you like to edit?", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            self.view.values = self.values
            self.view.stop()

class SuggestConfEditMainView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.add_item(SuggestConfEditMain(ctx))


class SuggsetConfDisableView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.value = None
        self.ctx = ctx
        
    @discord.ui.button(label="✅", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            self.value = True
            self.stop()
        
    @discord.ui.button(label="❌", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            self.value = False
            self.stop()

class SuggestSafeDecision(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        self.db = SuggestDB(bot.db)
        super().__init__()
        self.value = None

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, emoji="✅")
    async def enable(self, button: discord.ui.Button, interaction: discord.Interaction):
        guildconf = await self.db.getconf(interaction.guild.id)
        if not guildconf:
            return
        channel_id = guildconf[0]
        suggestion_id = ""
        ogembed = interaction.message.embeds[0]
        embed = interaction.message.embeds[0]
        numloop = [word for word in embed.footer.text if word.isdigit()]
        for num in numloop:
            suggestion_id += f"{num}"
        message = await interaction.channel.fetch_message(interaction.message.id)
        await message.edit(embed=ogembed, view=None)
        embed.insert_field_at(0, name="Upvotes", value="0", inline=True)
        embed.insert_field_at(1, name="Downvotes", value="0", inline=True)
        embed.insert_field_at(2, name="Total", value="0", inline=True)
        embed.colour = discord.Colour.gold()
        msg = await self.bot.get_channel(channel_id).send(embed=embed, view=SuggestVotes(self.bot))
        await self.db.confirm(int(suggestion_id), msg.id)
        self.stop()

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red, emoji="❌")
    async def disable(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        numloop = [word for word in embed.footer.text if word.isdigit()]
        suggestion_id = ""
        for num in numloop: suggestion_id += f"{num}"
        await self.db.remove(int(suggestion_id))
        channel = self.bot.get_channel(interaction.channel_id)
        message = await channel.fetch_message(interaction.message.id)
        await message.edit(embed=embed, view=None)
        self.stop()

class SuggestVotes(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        self.db = SuggestDB(bot.db)
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Upvote", style=discord.ButtonStyle.green, emoji="👍", custom_id="SuggestionUpvote")
    async def upvote(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        numloop = [word for word in embed.footer.text if word.isdigit()]
        suggestion_id = ""
        for num in numloop: suggestion_id += f"{num}"
        await self.db.updatevote(suggestion_id=int(suggestion_id), upvote=interaction.user.id)
        votes = await self.db.getvotes(int(suggestion_id))
        upvotes = votes[0][0]
        upvotes = len(literal_eval(upvotes))
        downvotes = votes[0][1]
        downvotes = len(literal_eval(downvotes))
        total = upvotes-downvotes
        if total == 0:
            embed.colour = discord.Colour.gold()
        elif total < 0:
            embed.colour = self.bot.red
        elif total > 0:
            embed.colour = discord.Colour.green()
        totalprefix = "+" if total > 0 else ""
        total = f"{totalprefix}{total}"
        embed.set_field_at(0, name="Upvotes", value=upvotes, inline=True)
        embed.set_field_at(1, name="Downvotes", value=downvotes, inline=True)
        embed.set_field_at(2, name="Total", value=total, inline=True)
        msg = await interaction.channel.fetch_message(interaction.message.id)
        await msg.edit(embed=embed, view=SuggestVotes(self.bot))

    @discord.ui.button(label="Downvote", style=discord.ButtonStyle.red, emoji="👎", custom_id="SuggestionDownvote")
    async def downvote(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        numloop = [word for word in embed.footer.text if word.isdigit()]
        suggestion_id = ""
        for num in numloop: suggestion_id += f"{num}"
        await self.db.updatevote(suggestion_id=int(suggestion_id), downvote=interaction.user.id)
        votes = await self.db.getvotes(int(suggestion_id))
        upvotes = votes[0][0]
        upvotes = len(literal_eval(upvotes))
        downvotes = votes[0][1]
        downvotes = len(literal_eval(downvotes))
        total = upvotes-downvotes
        if total == 0:
            embed.colour = discord.Colour.gold()
        elif total < 0:
            embed.colour = self.bot.red
        elif total > 0:
            embed.colour = discord.Colour.green()
        totalprefix = "+" if total > 0 else ""
        total = f"{totalprefix}{total}"
        embed.set_field_at(0, name="Upvotes", value=upvotes, inline=True)
        embed.set_field_at(1, name="Downvotes", value=downvotes, inline=True)
        embed.set_field_at(2, name="Total", value=total, inline=True)
        msg = await interaction.channel.fetch_message(interaction.message.id)
        await msg.edit(embed=embed, view=SuggestVotes(self.bot))

class Paginator(discord.ui.View):
    def __init__(self, ctx, pages, page=0, start_end=False, step_10=False):
        super().__init__(timeout=120)
        self.ctx = ctx
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
        self.add_item(PaginatorButton(label="◀", page=previous_page, style=discord.ButtonStyle.red))
        self.add_item(PaginatorButton(label=f"{self.page + 1} / {len(self.pages)}", style=discord.ButtonStyle.grey, disabled=True))
        next_page = self.page + 1
        if next_page > self.count - 1:
            next_page = 0
        self.add_item(PaginatorButton(label="▶", page=next_page, style=discord.ButtonStyle.green))
        for item in non_page_buttons:
            self.add_item(item)

class PaginatorButton(discord.ui.Button["Paginator"]):
    def __init__(self, label, style, row=0, page=None, disabled=False):
        super().__init__(style=style, label=label, row=row, disabled=disabled)
        self.page = page

    async def callback(self, interaction: discord.Interaction):
        self.pages = self.view.pages
        self.view.page = self.page
        self.view.add_buttons()
        await interaction.message.edit(embed=self.pages[self.page], view=self.view)

