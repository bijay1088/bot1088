import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

class WarframeProfileCog(commands.Cog):
    def _init_(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Warframe Profile commands are online!")

    async def getProfileStats(self, ign):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.warframestat.us/profile/{ign}/stats') as request:
                try:
                    profilejson = await request.json()
                except Exception as e:
                    print(f"Failed to decode JSON: {e}")
                    return
        return profilejson
    

    async def getProfile(self, ign):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.warframestat.us/profile/{ign}') as request:
                try:
                    profilejson = await request.json()
                except Exception as e:
                    print(f"Failed to decode JSON: {e}")
                    return
        return profilejson

    #function to convert second to hours, minutes and seconds
    def secondsToHMS(self, seconds):
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
        timePlayed = f"{hours} hours, {minutes} minutes, {seconds} seconds"
        return timePlayed
    
    #convert iso to date
    def isoToDate(self, iso):
        date = iso.split('T')[0]
        return date


    #sort most used abilities
    def sortAbilities(self, abilities):
        abilities = sorted(abilities, key=lambda x: x['used'], reverse=True)
        return abilities
    
    #sort high scored kdrives
    def sortKdrive(self, kdrive):
        kdrive = sorted(kdrive, key=lambda x: x['highScore'], reverse=True)
        return kdrive

    #replace ability name
    def replaceAbilityName(self, ability):
        ability = ability.split('/')[-1].replace('Ability', '')
        return ability

    @app_commands.command(name="profile", description="Send profile info.")
    async def profile(self, interaction: discord.Interaction, ign: str):
        try:
            if ign == None:
                await interaction.response.send_message("Please provide a username.", allowed_mentions=discord.AllowedMentions(users=[interaction.user]))
                return
            await interaction.response.defer()
            profileStatsData = await self.getProfileStats(ign)
            profileData = await self.getProfile(ign)
            if profileStatsData == None or profileData == None:
                await interaction.followup.send("Failed to get profile data.", allowed_mentions=discord.AllowedMentions(users=[interaction.user]))
                return

            
            embed = discord.Embed(title=f"{profileData['displayName']}'s Profile", color=0x00ff00)
            embed.add_field(name="Mastery Rank", value=profileData['masteryRank'], inline=False)
            embed.add_field(name="Created", value=self.isoToDate(profileData['created']), inline=False)
            embed.add_field(name="Clan Name", value=profileStatsData['guildName'], inline=False)
            embed.add_field(name="Mission Completed vs Quit", value=f"{profileStatsData['missionsCompleted']} - {profileStatsData['missionsQuit']}" , inline=False)
            playTime = self.secondsToHMS(profileStatsData['timePlayedSec'])
            embed.add_field(name="Time Played", value=playTime, inline=False)
            
            await interaction.followup.send(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))
        except Exception as e:
            print(f"An error occured: {e}")
            await interaction.followup.send("An error occured. Please try again later.", allowed_mentions=discord.AllowedMentions(users=[interaction.user]))
        
    @app_commands.command(name="ability", description="Send most used ability.")
    async def ability(self, interaction: discord.Interaction, ign: str, limit: int = 5):
        try:
            if ign == None:
                await interaction.channel.send("Please provide a username.")
                return
            if limit < 1:
                await interaction.channel.send("Select the amount higher than 0")
                return
            profileStatsData = await self.getProfileStats(ign)
            profileData = await self.getProfile(ign)
            if profileStatsData == None:
                await interaction.channel.send("Failed to get profile data.")
                return

            embed = discord.Embed(title=f"{profileData['displayName']}'s most used ability", color=0x00ff00)
            abilities = self.sortAbilities(profileStatsData['abilities'])
            #display top 5 most used abilities
            if limit > len(abilities):
                limit = len(abilities)
            if limit > 20:
                limit = 20
            
            for i in range(limit):
                embed.add_field(name=f"{self.replaceAbilityName(abilities[i]['uniqueName'])}", value=f"Used: {abilities[i]['used']} times", inline=False)
            
            
            await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))

        except Exception as e:
            print(f"An error occured: {e}")
            await interaction.channel.send("An error occured. Please try again later.")
    
        
    @app_commands.command(name="kdrive", description="Send high scored kdrive races.")
    async def kdrive(self, interaction: discord.Interaction, ign: str):
        try:
            if ign == None:
                await interaction.channel.send("Please provide a username.")
                return
            profileStatsData = await self.getProfileStats(ign)

            if profileStatsData == None:
                await interaction.channel.send("Failed to get profile data.")
                return
            
            embed = discord.Embed(title=f"{ign}'s high scored kdrive races", color=0x00ff00)
            kdrive = self.sortKdrive(profileStatsData['kDriveRaces'])
            #display top 5 high scored
            if len(kdrive) > 5:
                limit = 5
            else:
                limit = len(kdrive)
            for i in range(limit):
                embed.add_field(name=f"{kdrive[i]['uniqueName']}", value=f"High Score: {kdrive[i]['highScore']}", inline=False)

            await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))
        except Exception as e:
            print(f"An error occured: {e}")
            await interaction.channel.send("An error occured. Please try again later.")
        
            
        




async def setup(bot):
    await bot.add_cog(WarframeProfileCog(bot))