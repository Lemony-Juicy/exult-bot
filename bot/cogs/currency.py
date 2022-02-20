import random

import discord
from discord.ext import commands

import random
import discord
from discord.ext import commands

from bot import read, write

class Economy:
    """Some discord bot CMDs: rob, beg, shop, buy, work, sell, fight"""

    def __init__(self):
        self.wallet = read('manage2.json', 'wallet', 1)  # read from database
        self.bank = read('manage2.json', 'bank', 1)  # read from database
        self.bank_limit = read('manage2.json', 'bank_limit', 1)  # read from database

    def update(self):  # modify this so it updates the wallet money, bank money, and bank limit of a user with sql
        # eg: def update(self, user_id: int, wallet=None, bank=None, bank_limit=None):
        #         and all ur sql shenanigans here
        write('manage2.json', self.wallet, 'wallet')
        write('manage2.json', self.bank, 'bank')
        write('manage2.json', self.bank_limit, 'bank_limit')

    def get_bank_limit(self, user_id):
        return DEFAULT_BANK_LIMIT if user_id not in self.bank_limit else self.bank_limit[user_id]

    def get_wallet(self, user_id):
        return 0 if self.wallet.get(user_id) is None else self.wallet.get(user_id)

    def get_bank(self, user_id):
        return 0 if self.bank.get(user_id) is None else self.bank.get(user_id)

    def increase_bank_limit(self, user_id):  # write to db
        if user_id not in self.bank_limit:
            self.bank_limit[user_id] = int(DEFAULT_BANK_LIMIT + DEFAULT_BANK_LIMIT * random.uniform(0.07, 0.35))
        else:
            self.bank_limit[user_id] += 1000000 // (self.bank_limit[user_id] * random.uniform(0.33, 2.00))
        self.update()
        return self.bank_limit[user_id]

    def increase_bank(self, user_id: int, amount: int) -> int:  # write to db
        """If the amount to put into bank is exceeding the bank limit, it will send back the amount of money needed
         to put back into the wallet"""
        bank = self.get_bank(user_id)
        bank_limit = self.get_bank_limit(user_id)
        if user_id in self.bank:
            if amount + bank > bank_limit:
                self.bank[user_id] = bank_limit
                self.update()
                return (amount + bank) - bank_limit
            self.bank[user_id] += amount
            self.update()
            return 0
        if amount + bank > bank_limit:
            self.bank[user_id] = bank_limit
            self.update()
            return (amount + bank) - bank_limit
        self.bank[user_id] = amount
        self.update()
        return 0

    def decrease_bank(self, user_id: int, amount) -> int:  # write to db
        if user_id in self.bank:
            bank = self.bank[user_id]
            if amount > bank:
                self.bank[user_id] -= bank
                self.update()
                return bank
            self.bank[user_id] -= amount
            self.update()
            return amount
        self.bank[user_id] = 0
        self.update()
        return 0

    def increase_wallet(self, user_id: int, amount):  # write to db
        self.wallet[user_id] = amount + self.wallet[user_id] if user_id in self.wallet else amount
        self.update()

    def decrease_wallet(self, user_id: int, amount):  # write to db
        if user_id in self.wallet:
            if self.wallet[user_id] - amount < 0:
                self.wallet[user_id] = 0
                amount_decreased = self.wallet[user_id]
                self.wallet[user_id] = 0
                self.update()
                return amount_decreased

            self.wallet[user_id] -= amount
            self.update()
            return amount
        self.wallet[user_id] = 0
        self.update()
        return self.decrease_bank(user_id, amount)

    async def send_balance(self, member: discord.Member, channel: discord.TextChannel):
        async with channel.typing():
            wallet = self.wallet.get(member.id)
            bank = self.bank.get(member.id)
            wallet = 0 if wallet is None else wallet
            bank = 0 if bank is None else bank
            embed = discord.Embed(
                description=f"``wallet``\n```yaml\n🌕 {wallet}```\n``bank``\n```fix\n🌕 {bank}  /  {self.get_bank_limit(user_id=member.id)}```")
            embed.set_author(icon_url=member.avatar.url, name=f"{str(member)}'s current Balance")
        await channel.send(embed=embed)

    def transfer_to_bank(self, user_id: int, amount=0, all_=False) -> int:  # write to db
        """If this function returns false, it indicates that the requested amount to be transferred is higher than the
        actual wallet, so the max amount is transferred. if true, there is no logical error. regardless of which bool
        this returns, the money will still be transferred."""
        wallet = self.get_wallet(user_id)
        if amount > wallet or all_:  # if amount to transfer is larger than the current balance:
            self.decrease_wallet(user_id, wallet)
            bank_leftover = self.increase_bank(user_id, wallet)
            self.increase_wallet(user_id, bank_leftover)
            return wallet - bank_leftover
        self.decrease_wallet(user_id, amount)
        self.increase_bank(user_id, amount)
        return amount

    def transfer_to_wallet(self, user_id: int, amount=0, all_=False) -> int:  # write to db
        """If this function returns false, it indicates that the requested amount to be transferred is higher than the
        actual bank, so the max amount is transferred. if true, there is no logical error. regardless of which bool
        this returns, the money will still be transferred."""
        bank = self.get_bank(user_id)
        if amount > bank or all_:  # if amount to transfer is larger than the current balance:
            self.decrease_bank(user_id, bank)
            self.increase_wallet(user_id, bank)
            return bank
        self.decrease_bank(user_id, amount)
        self.increase_wallet(user_id, amount)
        return amount

def check_item(func):
    """decorator for checking whether the use even has the item they are about to use"""
    async def wrapper(self, ctx, user):
        name = func.__name__.replace('use_', '').replace('_', ' ')
        if Items.names()[0][name] not in self.inventory.get_items(user):
            await ctx.send("You don't even have this item 🤡")
        else:
            await func(self, ctx, user)
    return wrapper

class Items:
    """In this class you can make use cmds, that will automatically run when the cmd .use [item] is ran. Just make sure
    to name the async method user_[and the item name (space replaced with underscore)]. so eg:
    if you want to execute a task when the user does .use fried chicken, you create an async method called
    use_fried_chicken(ctx, user), that passes in two arguments (the first is the context, and second is the user)"""
    #  collectibles
    glow_stone = 1
    star = 2
    gold = 3
    silver = 4
    platinum = 5
    shrek = 6
    # tools
    fairy_dust = 7  # Get 100% chance that ur gonna get an item when fishing
    bomb = 8
    bank_extender = 9  # Extends ur bank limit by 7 to 35% on the first time, then by a rational function
    metal_detector = 10
    bank_logger = 13
    fried_chicken = 14
    radioactive_cheese = 15
    shiny_hat = 16  # Automatically used to get more money when begging
    fishing_rod = 17  # Use to find other items: 1 in 75 chance of breaking
    eyeglass = 18  # Use this to search for random money or other items

    def __init__(self, inventory):
        self.inventory = inventory

    async def break_item(self, ctx: commands.Context, n: int, item, user,
                         message="Oh no! your {} broke. How unfortunate.."):
        name = self.inventory.all_items_enum[item]
        message = message.replace('{}', name)
        if random.randint(1, n) == 1:
            self.inventory.deduct_item(item=item, user=user)
            await warning(ctx, message)
            return True

    @check_item
    async def use_fishing_rod(self, ctx: commands.Context, user):
        if await self.break_item(ctx, 75, Items.eyeglass, user):
            return
        else:
            if random.randint(1, 5) == 2 or Items.fairy_dust in self.inventory.get_items(user):
                items = COLLECTIBLES.copy()
                items.extend([Items.bank_extender, Items.bomb, Items.shiny_hat, Items.bank_extender])
                random_item = random.choice(items)
                await ctx.send(f"You obtained a ``{self.inventory.all_items_enum[random_item]}``")
                self.inventory.add_item(random_item, user)
            else:
                await ctx.send("you got attacked by a fish, leaving you no option but to leave promptly..")

    @check_item
    async def use_bomb(self, ctx: commands.Context, user: discord.Member):
        """reign some havoc. Using the bomb will wipe our a portion of some random unlucky person in the server."""
        members = ctx.guild.members
        members.remove(user)
        for member in members:
            if member.bot:
                members.remove(member)
        user = random.choice(members)
        if random.randint(1, 10) != 5:
            victim_money = self.inventory.get_wallet(user.id)
            destroy_money = int(victim_money * (random.randint(20, 60) / 100))
            self.inventory.decrease_wallet(user.id, destroy_money)
            await ctx.send(
                f"You successfully bombed {user.mention}'s wallet, annihilating {destroy_money} coins from them")
        else:
            await ctx.send("Unfortunately, the bomb didn't work. What a tragedy")
        self.inventory.deduct_item(Items.bomb, user)

    @check_item
    async def use_bank_extender(self, ctx: commands.Context, user: discord.Member):
        await ctx.send(f"You have successfully used your bank extender, and now can store a max of "
                       f"``{self.inventory.increase_bank_limit(user_id=user.id)} coins``")
        self.inventory.deduct_item(Items.bank_extender, user)

    @check_item
    async def use_eyeglass(self, ctx: commands.Context, user: discord.Member):
        if await self.break_item(ctx, 3, Items.eyeglass, user, f"Unfortunately, your eyeglass broke 😥"):
            return
        if random.randint(1, 5) == 2 or Items.fairy_dust in self.inventory.get_items(user):  # give money
            coins = random.randint(2, 200)
            self.inventory.increase_wallet(user.id, coins)
            return await ctx.send(f"You obtained {coins} coins from searching with the eyeglass")
        if random.randint(1, 5) == 2:
            items = [Items.bomb, Items.bank_extender, Items.eyeglass, Items.fried_chicken]
            chosen = random.choice(items)
            self.inventory.add_item(chosen, user)
            return await ctx.send(f"You found {self.inventory.all_items_enum[chosen]} and took it.")
        await ctx.send("You didn't find anything, loser")

    @check_item
    async def use_metal_detector(self, ctx: commands.Context, user: discord.Member):
        if await self.break_item(ctx, 75, Items.eyeglass, user):
            return
        if random.randint(1, 3) == 2 or Items.fairy_dust in self.inventory.get_items(user):  # give money
            coins = random.randint(20, 500)
            self.inventory.increase_wallet(coins)
            return await ctx.send(f"You found {coins} coins")
        if random.randint(1, 6) == 2:
            items = [Items.gold, Items.silver, Items.platinum, Items.shrek]
            items.extend([Items.fairy_dust] * 4)
            chosen = random.choice(items)
            self.inventory.add_item(chosen, user)
            return await ctx.send(f"You found {self.inventory.all_items_enum[chosen]}")
        await ctx.send("You didn't find anything, loser")

    @staticmethod
    def names():
        """all_items_str has key values of strings, whereas all_items_enum has key values of ints. use this to get
        the name of the item"""
        all_items_str = {}
        all_items_enum = {}
        for name in vars(Items):
            if not name.startswith('__'):
                name_enum = eval(f"{Items.__name__}.{name}")
                if isinstance(name_enum, int):
                    all_items_str[name.replace('_', ' ')] = name_enum
                    all_items_enum[name_enum] = name.replace('_', ' ')
        return all_items_str, all_items_enum


SHOP_ITEMS = {Items.glow_stone: 75000, Items.star: 10000, Items.fairy_dust: 55,
              Items.fishing_rod: 1300, Items.fried_chicken: 175, Items.shiny_hat: 100, Items.shrek: 2500, Items.bomb: 5000,
              Items.radioactive_cheese: 25000, Items.metal_detector: 15000, Items.eyeglass: 75}

COLLECTIBLES = [Items.star, Items.glow_stone, Items.gold, Items.platinum, Items.silver, Items.shrek]
USE_ITEMS = [Items.bomb, Items.bank_extender, Items.fishing_rod, Items.metal_detector]
POWER_UPS = [Items.shiny_hat, Items.fairy_dust]


async def warning(ctx, msg):
    await ctx.send(
        embed=discord.Embed(description=msg, colour=0xff0000))


async def success(ctx: commands.Context, msg):
    await ctx.send(
        embed=discord.Embed(description=msg, colour=0x00ff00).set_footer(icon_url=ctx.author.avatar.url))


class Inventory(Economy):
    def __init__(self):
        """self.inventory keeps track of all user's inventory items, and quantity"""
        self.inventory = {}  # read('manage2.json', 'inventory', 2)  # read from database
        self.all_items_str, self.all_items_enum = Items.names()
        self.itemInteractions = Items(self)
        super().__init__()

    async def check_item(self, ctx, item) -> bool:
        item = self.all_items_str.get(item)
        if item is None:
            await warning(ctx, "This is not a valid item in the shop, silly")
            return False
        return True

    async def get_items(self, user) -> dict:
        x = economy.EconomyDB(self.bot.db)
        return await x.get_balance(user)

    async def update_inv(self, user, bal):
        # do sql db stuff here again like the update method in Economy
        write('manage2.json', self.inventory, 'inventory')
        x = economy.EconomyDB(self.bot.db)
        await x.update_inventory(user, bal)

    async def buy(self, ctx: commands.Context, item_name: str):
        if not await self.check_item(ctx, item_name):
            return
        user = ctx.author
        item = self.all_items_str.get(item_name)
        price = SHOP_ITEMS[item]
        if self.get_wallet(user.id) < price:
            return await warning(ctx, "You **do not have enough money** in ``your wallet`` to buy this 👽")
        self.add_item(item, user)
        self.decrease_wallet(user.id, price)
        await success(ctx, f"Successfully bought ``{item_name}`` for ``{price} coins``")

    def add_item(self, item, user):
        """Can parse in the int (enum) value of the item, or the name of the item"""
        if isinstance(item, str):
            item = self.all_items_str[item.lower()]
        if user.id in self.inventory:
            self.inventory[user.id][item] = self.inventory[user.id][item] + 1 if item in self.inventory[user.id] else 1
        else:
            self.inventory[user.id] = {item: 1}
        self.update_inv()

    def deduct_item(self, item, user: discord.Member):
        """Can parse in the int (enum) value of the item, or the name of the item"""
        if isinstance(item, str):
            item = self.all_items_str[item.lower()]
        try:
            if self.inventory[user.id][item] - 1 <= 0:
                del self.inventory[user.id][item]
            else:
                self.inventory[user.id][item] -= 1
            self.update_inv()
            return True
        except KeyError:
            return False

    async def sell(self, ctx: commands.Context, item_name: str):
        if not await self.check_item(ctx, item_name):
            return
        item = self.all_items_str.get(item_name)  # type: int
        price = SHOP_ITEMS[item]
        user = ctx.author
        if self.deduct_item(item, user):
            self.increase_wallet(user.id, price)
            await success(ctx, f"Successfully sold ``{item_name}`` for ``{price} coins``")
            return
        await warning(ctx, "You don't Even have this item 🤦🏻‍♂️")

    async def send_inventory(self, ctx: commands.Context, user: discord.Member):
        userInv = self.get_items(user)
        if not userInv:
            return await warning(ctx, "You do not have anything in your inventory 😞")
        async with ctx.typing():
            user_items = []
            for item in userInv:
                user_items.append(f"```py\n{self.all_items_enum[item]}: {userInv[item]}```")
        await ctx.reply(embed=discord.Embed(title=f"{user}'s Inventory", description=''.join(user_items),
                                            colour=discord.Colour.random()))

    async def send_shop(self, ctx: commands.Context):
        async with ctx.typing():
            items = []
            for item in SHOP_ITEMS:
                items.append(f"{self.all_items_enum[item]}: ``{SHOP_ITEMS[item]}🌕``")
        await ctx.send(embed=discord.Embed(title="Shop items", description='\n'.join(items),
                                           colour=discord.Colour.dark_orange()))

    async def use(self, ctx, item, user):
        item = item.lower()
        method_name = f"use_{item.replace(' ', '_')}"
        if method_name in vars(Items):
            await Items.__getattribute__(self.itemInteractions, method_name)(ctx, user)
        else:
            await warning(ctx, "This isn't a valid item to be used you baboon")


DEFAULT_BANK_LIMIT = 999999


def beg_phrases():
    BEG_PHRASES = {0: "joe biden spat on you",
                   random.randint(20,
                                  60): "joe mama found you on the street and decided to give you {} coins from some of her savings",
                   random.randint(100, 200): "Some rich bozo gave you {} out of pity",
                   -random.randint(12, 50): "You got robbed by some rascal. {}",
                   random.randint(12, 50): "someone threw {} coins at you ",
                   random.randint(1,
                                  100): "You successfully gained {} coins from the act of passively screaming for money "
                                        "whilst reminiscing the quite unsuccessful path you took"}
    money = []
    for money_ in BEG_PHRASES:
        money.append(money_)
    selected_money = random.choice(money)
    return [selected_money, BEG_PHRASES[selected_money]]


class ItemInteractions:
    def __init__(self, economy: Inventory, bot: commands.Bot):
        self.economy = economy
        self.bot = bot

    async def beg(self, user: discord.Member):
        original_money, phrase = beg_phrases()
        multiplier = round(random.uniform(0.5, 1.2), 2)
        if Items.shiny_hat in await self.economy.get_items(user):
            money = round(abs(original_money) * multiplier) + original_money if original_money >= 0 else 0
            if money > 0:
                phrase += f"\n(You got ``{int(multiplier * 100)}%`` more because of the shiny hat!)"
            else:
                phrase = phrase.replace('{}',
                                        f"However, you somehow managed to regain back all the stolen coins with the powers of shiny hat")
            self.economy.deduct_item(Items.shiny_hat, user)
            self.economy.increase_wallet(user.id, money)
            return phrase.replace('{}', f"{original_money}")
        if original_money < 0:
            original_money = self.economy.decrease_wallet(user.id, abs(original_money))
            phrase = phrase.replace('{}', f'They mugged off a grand total of {original_money} coins off you 😞')
        else:
            self.economy.increase_wallet(user.id, original_money)
        return phrase.replace('{}', f"{original_money}")


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.economy = Inventory()
        self.interactions = ItemInteractions(self.economy, self.bot)

    @commands.command(aliases=['bal'])
    async def balance(self, ctx: commands.Context, user: discord.Member = None):
        await self.economy.send_balance(ctx.author if user is None else user, ctx.channel)

    @balance.error
    async def balance_error(self, ctx, error):
        await badArg(ctx, error, "You need to mention someone to view their balance, silly. To view your balance, just "
                                 "do the command, but without any arguments")

    @commands.command()
    @commands.cooldown(1, random.randint(30, 120))
    async def beg(self, ctx):
        await ctx.send(await self.interactions.beg(user=ctx.author))

    @commands.command()
    @commands.cooldown(1, random.randint(60, 120))
    async def rob(self, ctx: commands.Context, user: discord.Member):
        user_money = self.economy.get_wallet(user.id)
        if user_money < 100:
            return await ctx.send(
                embed=discord.Embed(description="This user doesn't have enough money in their wallet, "
                                                "or is too poor, so you are legally obliged by law to not rob them",
                                    colour=0xff0000))
        rob_money = random.randint(1, 83)
        if random.randint(1, 4) != 2:
            amount_taken = self.economy.decrease_wallet(user.id, rob_money)
            self.economy.increase_wallet(ctx.author.id, amount_taken)
            await ctx.send(
                embed=discord.Embed(description=f"Successfully robbed {rob_money} off {user}", colour=0xff0000))
        else:
            dec = random.randint(15, 60)
            amount_decreased = self.economy.decrease_wallet(ctx.author.id, dec)
            self.economy.increase_wallet(user.id, amount_decreased)
            await ctx.send(f"You got caught and {user} spanked you, and took {amount_decreased} coins away with them")

    @commands.command()
    async def shop(self, ctx):
        await self.economy.send_shop(ctx)

    @commands.command()
    async def buy(self, ctx, *, item):
        await self.economy.buy(ctx, item)

    @commands.command()
    async def sell(self, ctx, *, item):
        await self.economy.sell(ctx, item)

    @commands.command(aliases=['in'])
    async def inventory(self, ctx):
        await self.economy.send_inventory(ctx, ctx.author)

    @commands.command()
    async def use(self, ctx, *, item):
        await self.economy.use(ctx, item, ctx.author)

    @commands.command(aliases=['dep', 'transfer'])
    async def deposit(self, ctx, amount):
        if not amount.isdigit() and amount.lower() != 'all':
            return await warning(ctx,
                                 "⚠ You need to provide an amount of money to transfer to the bank. type 'all' instead "
                                 "of an amount to transfer all the money")
        if self.economy.get_bank(user_id=ctx.author.id) >= self.economy.get_bank_limit(user_id=ctx.author.id):
            return await warning(ctx,
                                 "⚠ You **cannot deposit** anymore money into your bank since the **maximum bank limit is reached**. "
                                 "To increase this amount you can either **buy the bank extender** item, or gain it from using other items")
        async with ctx.typing():
            if amount.lower() == 'all':
                transferred = self.economy.transfer_to_bank(ctx.author.id, all_=True)
            else:
                amount = int(amount)
                transferred = self.economy.transfer_to_bank(ctx.author.id, amount)
        await success(ctx, f"Transferred, {transferred} coins to bank.")

    @commands.command(aliases=['take'])
    async def withdraw(self, ctx, amount):
        if not amount.isdigit() and amount.lower() != 'all':
            return await warning(ctx,
                                 "⚠ You need to provide an amount of money to transfer to the bank. type 'all' instead "
                                 "of an amount to transfer all the money")
        async with ctx.typing():
            if amount.lower() == 'all':
                transferred = self.economy.transfer_to_wallet(ctx.author.id, all_=True)
            else:
                amount = int(amount)
                transferred = self.economy.transfer_to_wallet(ctx.author.id, amount)
        await success(ctx, f"Withdrew {transferred} coins from bank to wallet.")


def setup(bot: commands.Bot):
    bot.add_cog(Currency(bot))
