import discord
from discord import app_commands
from discord.ext import commands
import math
import random

class FunCog(commands.Cog):
    def _init_(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun commands are online!")

    
    @app_commands.command(name="roll", description="Roll a dice.")
    async def roll(self, interaction:discord.Interaction, sides:int):
        rolled = random.randint(1, sides)
        embed = discord.Embed(title="Dice Roll")
        embed.add_field(name="Result", value=rolled)
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))


    @app_commands.command(name="coinflip", description="Flip a coin.")
    async def coinflip(self, interaction:discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        embed = discord.Embed(title="Coin Flip")
        embed.add_field(name="Result", value=result)
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))


async def setup(bot):
    await bot.add_cog(FunCog(bot))