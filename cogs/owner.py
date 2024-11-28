import discord
from discord import app_commands
from discord.ext import commands
import math
import random

class OwnerCog(commands.Cog):
    def _init_(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner commands are online!")

    @app_commands.command(name="shutdown", description="Shutdown bot.")
    async def shutdown(self, interaction:discord.Interaction,):
        if interaction.user.id != 563257720321474580:
            await interaction.response.send_message("You are not the owner lol.")
            return
        await interaction.response.send_message(f"Shutting down...")
        await interaction.client.close()


async def setup(bot):
    await bot.add_cog(OwnerCog(bot))