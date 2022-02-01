import discord
from . import helpembeds as he
from .embedbuilder import EmbedBuilder
from database.ticket import TicketDB
import string
import ast
import random
from urllib.parse import quote_plus
from ast import literal_eval

from database.suggestions import SuggestDB

class HelpBase:
    
    class Dropdown(discord.ui.Select):
        def __init__(self, ctx, bot):
            self.ctx = ctx
            self.bot = bot

            options = [
                discord.SelectOption(label="Main Menu", value="Main Menu"),
                discord.SelectOption(label="News", value="News"),
                discord.SelectOption(label="Moderation", value="Moderation"),
                discord.SelectOption(label="Miscellaneous", value="Miscellaneous"),
                discord.SelectOption(label="Utility", value="Utility"),
                discord.SelectOption(label="Music", value="Music"),
                discord.SelectOption(label="Fun", value="Fun"),
                discord.SelectOption(label="Economy", value="Economy"),
                discord.SelectOption(label="Configuration", value="Configuration")
            ]
            super().__init__(placeholder="What command category would you like to view?", options=options)

        async def callback(self, interaction: discord.Interaction):
            if interaction.data["values"] == ["Main Menu"]:
                await interaction.message.edit(embed=he.HelpEmbeds(self.ctx, self.bot).mainmenu())
            if interaction.data["values"] == ["News"]:
                await interaction.message.edit(embed=he.HelpEmbeds(self.ctx, self.bot).news())
            if interaction.data["values"] == ["Moderation"]:
                await interaction.message.edit(embed=he.HelpEmbeds(self.ctx, self.bot).moderation())
            if interaction.data["values"] == ["Miscellaneous"]:
                await interaction.message.edit(embed=he.HelpEmbeds(self.ctx, self.bot).miscellaneous())
            if interaction.data["values"] == ["Utility"]:
                await interaction.message.edit(embed=he.HelpEmbeds(self.ctx, self.bot).utility())
            if interaction.data["values"] == ["Music"]:
                await interaction.message.edit(embed=he.HelpEmbeds(self.ctx, self.bot).music())
            if interaction.data["values"] == ["Fun"]:
                await interaction.message.edit(embed=he.HelpEmbeds(self.ctx, self.bot).fun())
            if interaction.data["values"] == ["Economy"]:
                await interaction.message.edit(embed=he.HelpEmbeds(self.ctx, self.bot).economy())
            if interaction.data["values"] == ["Configuration"]:
                await interaction.message.edit(embed=he.HelpEmbeds(self.ctx, self.bot).configuration())
        
    class DropdownView(discord.ui.View):
        def __init__(self, ctx, bot):
            super().__init__()
            self.add_item(HelpBase.Dropdown(ctx, bot))
            
class TicketSetupPanelCat:
    
    class Dropdown(discord.ui.Select):
        def __init__(self, ctx):
            self.ctx = ctx
            options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.ctx.guild.categories]
            super().__init__(placeholder="Category where the channel you want the panel to be sent is in", options=options, min_values=1, max_values=1)
            
        async def callback(self, interaction: discord.Interaction):
            self.view.values = self.values
            self.view.stop()
            
    
    class DropdownView(discord.ui.View):
        def __init__(self, ctx):
            self.ctx = ctx
            super().__init__()
            self.add_item(TicketSetupPanelCat.Dropdown(self.ctx))
            
class TicketSetupPanelChan:
    
    class Dropdown(discord.ui.Select):
        def __init__(self, cat):
            self.cat = cat
            options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.cat.text_channels]
            super().__init__(placeholder="Select the channel where you want the ticket panel to send", options=options, min_values=1, max_values=1)
            
        async def callback(self, interaction: discord.Interaction):
            self.view.values = self.values
            self.view.stop()
            
    class DropdownView(discord.ui.View):
        def __init__(self, cat):
            self.cat = cat
            super().__init__()
            self.add_item(TicketSetupPanelChan.Dropdown(self.cat))
            
class TicketCategory:
    
    class Dropdown(discord.ui.Select):
        def __init__(self, ctx):
            self.ctx = ctx
            options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.ctx.guild.categories]
            super().__init__(placeholder="Category where the channel you want the tickets to be created in", options=options, min_values=1, max_values=1)
            
        async def callback(self, interaction: discord.Interaction):
            self.view.values = self.values
            self.view.stop()
            
    class DropdownView(discord.ui.View):
        def __init__(self, ctx):
            self.ctx = ctx
            super().__init__()
            self.add_item(TicketCategory.Dropdown(self.ctx))
            
class TicketSetupLogCat:
    
    class Dropdown(discord.ui.Select):
        def __init__(self, ctx):
            self.ctx = ctx
            options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.ctx.guild.categories]
            super().__init__(placeholder="Category where the channel you want the logs to be sent is in", options=options, min_values=1, max_values=1)
            
        async def callback(self, interaction: discord.Interaction):
            self.view.values = self.values
            self.view.stop()
            
    
    class DropdownView(discord.ui.View):
        def __init__(self, ctx):
            self.ctx = ctx
            super().__init__()
            self.add_item(TicketSetupLogCat.Dropdown(self.ctx))
            
class TicketSetupLogChan:
    
    class Dropdown(discord.ui.Select):
        def __init__(self, cat):
            self.cat = cat
            options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.cat.text_channels]
            super().__init__(placeholder="Select the channel where you want the ticket embed to send", options=options, min_values=1, max_values=1)
            
        async def callback(self, interaction: discord.Interaction):
            self.view.values = self.values
            self.view.stop()
            
    class DropdownView(discord.ui.View):
        def __init__(self, cat):
            self.cat = cat
            super().__init__()
            self.add_item(TicketSetupLogChan.Dropdown(self.cat))
            
class TicketSetupConfirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        
    @discord.ui.button(label="✅", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Sending Ticket...", ephemeral=True)
        self.value = True
        self.stop()
        
    @discord.ui.button(label="❌", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Cancelling ticket panel setup...", ephemeral=True)
        self.value = False
        self.stop()
        
class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="❌", custom_id="CloseTicket")
    async def closeticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        return

class OpenTicket(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji="📥", custom_id="OpenTicket")
    async def openticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        return
    
class LogsBase:
    
    class Dropdown(discord.ui.Select):
        def __init__(self):
            options = [
                discord.SelectOption(label="All", value="All"),
                discord.SelectOption(label="Create channels for me", value="Create"),
                discord.SelectOption(label="Channel Logs", value="ChannelLogs"),
                discord.SelectOption(label="Server Logs", value="ServerLogs"),
                discord.SelectOption(label="Member Logs", value="MemberLogs"),
                discord.SelectOption(label="Message Logs", value="MessageLogs"),
                discord.SelectOption(label="Voice Logs", value="VoiceLogs"),
                discord.SelectOption(label="Ticket Logs", value="TicketLogs")
            ]
            super().__init__(placeholder="What log channel would you like to configure?", options=options)

        async def callback(self, interaction: discord.Interaction):
            self.view.values = self.values
            self.view.stop()
        
    class DropdownView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(LogsBase.Dropdown())
            
class Avatar(discord.ui.View):
    def __init__(self, link: str, member: discord.Member):
        super().__init__()
        self.add_item(discord.ui.Button(label=f"{member}'s avatar", url=link))

class SuggestConfCat(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.ctx.guild.categories]
        super().__init__(placeholder="Select the Category that your desired suggestions channel is in", options=options, min_values=1, max_values=1)
        
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            self.view.values = self.values
            self.view.stop()

class SuggestConfCatView(discord.ui.View):
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__()
        self.add_item(SuggestConfCat(ctx))

class SuggestConfChan(discord.ui.Select):
    def __init__(self, cat, ctx):
        self.cat = cat
        self.ctx = ctx
        options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.cat.text_channels]
        super().__init__(placeholder="Select the channel where you want suggestions to be sent", options=options, min_values=1, max_values=1)
        
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            self.view.values = self.values
            self.view.stop()
        
class SuggestConfChanView(discord.ui.View):
    def __init__(self, cat, ctx):
        self.cat = cat
        super().__init__()
        self.add_item(SuggestConfChan(self.cat, ctx))

class SuggestConfSafemode(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.value = None
        self.ctx = ctx

    @discord.ui.button(label="Enable", style=discord.ButtonStyle.green, emoji="✅")
    async def enable(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            self.value = True
            self.stop()

    @discord.ui.button(label="Disable", style=discord.ButtonStyle.red, emoji="❌")
    async def disable(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            self.value = False
            self.stop()

class SuggestConfSafeCat(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.ctx.guild.categories]
        super().__init__(placeholder="Select the Category for the channel that you want suggestions to await acceptance in.", options=options, min_values=1, max_values=1)
        
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            self.view.values = self.values
            self.view.stop()

class SuggestConfCatSafeView(discord.ui.View):
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__()
        self.add_item(SuggestConfSafeCat(ctx))

class SuggestConfSafeChan(discord.ui.Select):
    def __init__(self, cat, ctx):
        self.cat = cat
        self.ctx = ctx
        options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.cat.text_channels]
        super().__init__(placeholder="Select the channel that you want suggestions to await acceptance in.", options=options, min_values=1, max_values=1)
        
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            self.view.values = self.values
            self.view.stop()
        
class SuggestConfChanSafeView(discord.ui.View):
    def __init__(self, cat, ctx):
        self.cat = cat
        super().__init__()
        self.add_item(SuggestConfSafeChan(self.cat, ctx))

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

class SuggestConfEditChannelCat(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.ctx.guild.categories]
        super().__init__(placeholder="Select the Category for the channel that you want suggestions to await acceptance in.", options=options, min_values=1, max_values=1)
        
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            self.view.values = self.values
            self.view.stop()

class SuggestConfEditChannelCatView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.add_item(SuggestConfEditChannelCat(ctx))

class SuggestConfEditChannel(discord.ui.Select):
    def __init__(self, cat, ctx):
        self.cat = cat
        self.ctx = ctx
        options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.cat.text_channels]
        super().__init__(placeholder="Select the channel that you want suggestions to await acceptance in.", options=options, min_values=1, max_values=1)
        
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            self.view.values = self.values
            self.view.stop()

class SuggestConfEditChannelView(discord.ui.View):
    def __init__(self, cat, ctx):
        self.cat = cat
        super().__init__()
        self.add_item(SuggestConfEditChannel(self.cat, ctx))

class SuggestConfEditSafeCat(discord.ui.Select):
    def __init__(self, ctx, safemode):
        self.ctx = ctx
        options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.ctx.guild.categories]
        if safemode:
            options.insert(0, discord.SelectOption(label="Disable Safemode", value="Disable"))
        super().__init__(placeholder="Select the Category for the channel that you want suggestions to await acceptance in.", options=options, min_values=1, max_values=1)
        
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            self.view.values = self.values
            self.view.stop()

class SuggestConfEditSafeCatView(discord.ui.View):
    def __init__(self, ctx, safemode):
        super().__init__()
        self.add_item(SuggestConfEditSafeCat(ctx, safemode))

class SuggestConfEditSafeChannel(discord.ui.Select):
    def __init__(self, cat, ctx):
        self.cat = cat
        self.ctx = ctx
        options = [discord.SelectOption(label=l.name, value=str(l.id)) for l in self.cat.text_channels]
        super().__init__(placeholder="Select the channel that you want suggestions to await acceptance in.", options=options, min_values=1, max_values=1)
        
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            self.view.values = self.values
            self.view.stop()

class SuggestConfEditSafeChannelView(discord.ui.View):
    def __init__(self, cat, ctx):
        self.cat = cat
        super().__init__()
        self.add_item(SuggestConfEditSafeChannel(self.cat, ctx))

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