import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

class AnimalCog(commands.Cog):
    def _init_(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("Animal commands are online!")


    async def getFox(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://randomfox.ca/floof/?ref=apilist.fun') as request:
                try:
                    foxjson = await request.json()
                except Exception as e:
                    print(f"Failed to decode JSON: {e}")
                    return
        return foxjson['image']
    


    @app_commands.command(name="fox", description="Get a random fox image.")
    async def fox(self, interaction:discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://randomfox.ca/floof/?ref=apilist.fun') as request:
                try:
                    fox = await request.json()
                except Exception as e:
                    print(f"Failed to decode JSON: {e}")
                    return
        embed = discord.Embed(title="Fox")
        embed.set_image(url=fox)
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))


    @app_commands.command(name="dog", description="Get a random dog image.")
    async def dog(self, interaction:discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random') as request:
                try:
                    dogjson = await request.json()
                except Exception as e:
                    print(f"Failed to decode JSON: {e}")
                    return
        dog = dogjson['message']
        embed = discord.Embed(title="Dog")
        embed.set_image(url=dog)
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))

    @app_commands.command(name="cat", description="Get a random cat image.")
    async def cat(self, interaction:discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thecatapi.com/v1/images/search') as request:
                try:
                    catjson = await request.json()
                except Exception as e:
                    print(f"Failed to decode JSON: {e}")
                    return
        cat = catjson[0]['url']
        embed = discord.Embed(title="Cat")
        embed.set_image(url=cat)
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))

async def setup(bot):
    await bot.add_cog(AnimalCog(bot))



    