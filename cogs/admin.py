import discord
from discord import app_commands
from discord.ext import commands
import math
import random

class AdminCog(commands.Cog):
    def _init_(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin commands are online!")


    @app_commands.command(name="test", description="This is just a test.")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("Test")

    @app_commands.command(name="clear", description="Delete specific amount of messages.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction:discord.Interaction, amount: int):
        if amount <1:
            await interaction.channel.send("Select the amount hiugher than 0")
            return
        await interaction.response.defer()
        deleted_amount = await interaction.channel.purge(limit=amount+1)
        await interaction.channel.send(f"{interaction.user.mention} has deleted {len(deleted_amount)} messages.")

    @app_commands.command(name="kick", description="Kicks a user.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction:discord.Interaction, member: discord.Member):
        await interaction.guild.kick(member)
        await interaction.response.send_message(f"Kicked the user {member.mention}")
    

    @app_commands.command(name="ban", description="Bans a user.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction:discord.Interaction, member: discord.Member):
        await interaction.guild.ban(member)
        await interaction.response.send_message(f"Banned the user {member.mention}")

    @app_commands.command(name="unban", description="Unbans a user using id.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction:discord.Interaction, user_id: str):
        user = await self.bot.fetch_user(user_id)
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"Unbanned the user {user.name}")

async def setup(bot):
    await bot.add_cog(AdminCog(bot))