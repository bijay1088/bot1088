import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import asyncio
from itertools import cycle

# ephemeral = hidden only for you
#interaction.user.mention

bot=commands.Bot(command_prefix="b/", intents=discord.Intents.all())

load_dotenv()
token=os.getenv('token')

bot_statuses = cycle(["Hi there, Hello", "I am tired..."])

@tasks.loop(seconds = 60)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))

@bot.event
async def on_ready():
    print("Bot is running...")
    change_bot_status.start()
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error with syncing application commands has occured: ", e)




@bot.tree.command(name="ping", description="Shows latency of bot.")
async def ping(interaction: discord.Interaction):
    embed = discord.Embed(title="Pong!", color = discord.Color.red())
    embed.add_field(name=f"Latency in ms: ", value=f"{round(bot.latency * 1000)}ms.", inline=False)
    await interaction.response.send_message(embed=embed)


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")




async def main():
    async with bot:
        await load()
        await bot.start(token)

asyncio.run(main())


