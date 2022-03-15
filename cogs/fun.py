from discord import app_commands, Interaction, Object

import os
import requests as r

from utils import *

@app_commands.command(name="wtp", description="Who's that pokemon?")
async def wtp_slash(interaction: Interaction):
    headers = {"Authorization": os.getenv("DAGPI_TOKEN")}
    res = r.get("https://api.dagpi.xyz/data/wtp", headers=headers).json()
    
    question = res["question"]
    answer = res["answer"]
    
    lives = 3
    
    check = lambda m: m.author.id != interaction.client.user.id and m.channel.id == interaction.channel.id
    
    types = ", ".join(res["Data"]["Type"])
    
    embed = embed_builder(title="Who's that pokemon?", description=f"Type(s): {types}", image=question, 
                          fields=[["Guesses Remaining:", f"{lives}", True]],
                          footer=f"{answer}")
    view = PokemonGuess(answer)
    msg = await interaction.channel.send(embed=embed)
    final_answer = None
    while lives > 0 :
        await view.wait()
        guess = view.guess
        if guess.lower() == answer.lower():
            final_answer = answer
            
        lives -= 1
        embed.set_field_at(0, name="Guesses Remaining:", value=f"{lives}")
        view = PokemonGuess(answer)
        await msg.edit(embed=embed, view=view)
        
async def setup(bot):
    commands = [wtp_slash]
    guilds = [912148314223415316, 949429956843290724]
    for command in commands:
        bot.tree.add_command(command, guilds=[Object(guild) for guild in guilds])
        print(f"Added {command.name} to {guilds}")