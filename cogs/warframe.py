import json
import random
import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
<<<<<<< HEAD
from datetime import datetime, timedelta
=======
from datetime import datetime
>>>>>>> 8625a649efdad5e4e855ffba42f9e408769b9bf6
import re

class WarframeCog(commands.Cog):
    def _init_(self, bot):
        self.bot = bot

    #converting datetime string to timestamp
    def convertTimestamp(self, timeStr):
        try:
            dt = datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%S.%fZ")
            timestamp = dt.timestamp()
            return timestamp
        except Exception as e:
            print(f"Failed to convert timestamp: {e}")
            return None
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("Warframe commands are online!")


    
    #function to call warframe api and return the data
    async def getWarframeData(self, data):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/pc') as request:
                try:
                    warframejson = await request.json()
                except Exception as e:
                    print(f"Failed to decode JSON: {e}")
                    return
        return warframejson[data]
    
    #function to call warframe data from github
    async def getWarframeDataGithub(self, data):
        async with aiohttp.ClientSession() as session:
            link = f'https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/{data}.json'
            async with session.get(link) as request:
                try:
                    warframetext = await request.text()
                    warframetext = re.sub(r'^\s*//.*\n?', '', warframetext, flags=re.MULTILINE)
                    warframejson = json.loads(warframetext)
                        

                except Exception as e:
                    print(f"Failed to decode JSON: {e}")
                    return
        return warframejson

    async def getKuvaTenet(self, data):
        ktjson = await self.getWarframeDataGithub("Primary")
        ktjson = ktjson + (await self.getWarframeDataGithub("Secondary"))
        ktjson = ktjson + (await self.getWarframeDataGithub("Melee"))
        ktjson = [x for x in ktjson if data in x["name"]]
        return ktjson

    #image
    def getImageLink(self, name):
        imageLink = f'https://cdn.warframestat.us/img/{name}'
        return imageLink


    #anomoly
    @app_commands.command(name="anomaly", description="Send current anomaly.")
    async def anomaly(self, interaction: discord.Interaction):
        anomolyjson = await self.getWarframeData("sentientOutposts")
        if anomolyjson == None:
            await interaction.response.send_message("Something went wrong.")
            return
        
        embed = discord.Embed(title="Current Anomaly")
        embed.add_field(name="Node", value=f"{anomolyjson['mission']['node']} \n{anomolyjson['mission']['type']}")
        expiry_timestamp = self.convertTimestamp(anomolyjson["expiry"])
        embed.add_field(name="Ends", value=f"<t:{int(expiry_timestamp)}:R>", inline=False)
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))



    #archon
    @app_commands.command(name="archon", description="Send current archon hunt.")
    async def archon(self, interaction: discord.Interaction):

        missionjson = await self.getWarframeData("archonHunt")
        if missionjson == None:
            await interaction.response.send_message("Something went wrong.")
            return
        
        embed = discord.Embed(title="Current Archon Hunt")
        embed.add_field(name="Boss", value=missionjson["boss"])
        embed.add_field(name="Faction", value=missionjson["faction"])

        for i in range(3):
            mission_info = f"{missionjson['missions'][i]['nodeKey']} - {missionjson['missions'][i]['typeKey']}"
            embed.add_field(name=f"Mission {i + 1}", value=mission_info, inline=False)
        expiry_timestamp = self.convertTimestamp(missionjson["expiry"])  
        embed.add_field(name="Ends", value=f"<t:{int(expiry_timestamp)}:R>")

        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))



    #sortie
    @app_commands.command(name="sortie", description="Send current sortie.")
    async def sortie(self, interaction: discord.Interaction):
        sortiejson = await self.getWarframeData("sortie")
        if sortiejson is None:
            await interaction.response.send_message("Something went wrong.")
            return

        embed = discord.Embed(title="Current Sortie")

        # Add each mission with its type, node key, and modifier in one line
        for i in range(3):
            mission_info = f"{sortiejson['variants'][i]['missionTypeKey']} - {sortiejson['variants'][i]['nodeKey']}\nModifier: {sortiejson['variants'][i]['modifier']}"
            embed.add_field(name=f"Mission {i + 1}", value=mission_info, inline=False)

        expiry_timestamp = self.convertTimestamp(sortiejson["expiry"])
        embed.add_field(name="Ends", value=f"<t:{int(expiry_timestamp)}:R>")
        
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))

    #EDA



    #darvo deals
    @app_commands.command(name="darvo", description="Send current darvo deals.")
    async def darvo(self, interaction: discord.Interaction):
        darvojson = await self.getWarframeData("dailyDeals")
        if darvojson == None:
            await interaction.response.send_message("Something went wrong.")
            return

        embed = discord.Embed(title="Darvo Deals")
        embed.add_field(name="Item", value=darvojson[0]["item"])
        embed.add_field(name="Original Price", value=darvojson[0]["originalPrice"])
        embed.add_field(name="Sale Price", value=darvojson[0]["salePrice"])
        embed.add_field(name="Total", value=darvojson[0]["total"])
        embed.add_field(name="Sold", value=darvojson[0]["sold"])
        expiry_timestamp = self.convertTimestamp(darvojson[0]["expiry"])
        embed.add_field(name="Ends", value=f"<t:{int(expiry_timestamp)}:R>")
        
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))


    #alert
    @app_commands.command(name="alert", description="Send current alert.")
    async def alert(self, interaction: discord.Interaction):
        alertjson = await self.getWarframeData("alerts")
        if alertjson == None:
            await interaction.response.send_message("Something went wrong.")
            return

        embed = discord.Embed(title="Current Alert")
        for i in range(len(alertjson)): 
            expiry_timestamp = self.convertTimestamp(alertjson[i]["expiry"])
            alert_value = (
                f"{alertjson[i]['mission']['node']} - "
                f"{alertjson[i]['mission']['type']} - "
                f"\nExpiry: <t:{int(expiry_timestamp)}:R>\n"  
                f"Reward: {', '.join(alertjson[i]['mission']['reward']['items'])} + {alertjson[i]['mission']['reward']['credits']}"
            )
            
            embed.add_field(name=f"Alert {i + 1}", value=alert_value, inline=False)

        
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))


    #resurgence
    @app_commands.command(name="resurgence", description="Send current resurgence.")
    async def resurgence(self, interaction: discord.Interaction):
        resurgencejson = await self.getWarframeData("vaultTrader")
        if resurgencejson == None:
            await interaction.response.send_message("Something went wrong.")
            return

        embed = discord.Embed(title="Resurgence")
        total_schedule = len(resurgencejson["schedule"])
        if "item" not in resurgencejson["schedule"][total_schedule - 1]:
            total_schedule -= 1
        currentTimestamp = datetime.now().timestamp()
        current_schedule = "Not Available"
        next_schedule = "Not Available"

        try:
            if int(self.convertTimestamp(resurgencejson["schedule"][total_schedule - 2]['expiry'])) > int(currentTimestamp):
                current_schedule = resurgencejson["schedule"][total_schedule - 2]['item'].replace("M P V ", "")
                next_schedule = resurgencejson["schedule"][total_schedule -1]['item'].replace("M P V ", "")
            else:
                current_schedule = resurgencejson["schedule"][total_schedule - 1]['item'].replace("M P V ", "")
        except Exception as e:
            print(f"Failed to get the schedule: {e}")

        embed.add_field(name="Current Schedule", value=current_schedule, inline=False)
        embed.add_field(name="Next Schedule", value=next_schedule, inline=False)
        expiry_timestamp = self.convertTimestamp(resurgencejson["expiry"])
        embed.add_field(name="Ends", value=f"<t:{int(expiry_timestamp)}:R>")
        
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))

<<<<<<< HEAD
    """
=======

>>>>>>> 8625a649efdad5e4e855ffba42f9e408769b9bf6
    #alerts
    @app_commands.command(name="alert", description="Send current alert.")
    async def alert(self, interaction: discord.Interaction):
        alertjson = await self.getWarframeData("alerts")
        if alertjson == None:
            await interaction.response.send_message("Something went wrong.")
            return

        embed = discord.Embed(title="Current Alert")
        if len(alertjson) == 0:
            embed.add_field(name="Alert", value="No alert available.")
            await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))
            return
        
        for i in range(len(alertjson)): 
            expiry_timestamp = self.convertTimestamp(alertjson[i]["expiry"])
            alert_value = (
                f"{alertjson[i]['mission']['node']} - "
                f"{alertjson[i]['mission']['type']}"
                f"\nExpiry: <t:{int(expiry_timestamp)}:R>\n"  
                #f"Reward: {', '.join(alertjson[i]['mission']['reward']['itemString'])} + {alertjson[i]['mission']['reward']['credits']} credits"
                f"Reward: {(alertjson[i]['mission']['reward']['itemString'])} + {alertjson[i]['mission']['reward']['credits']} credits"
            )
            
            embed.add_field(name=f"Alert {i + 1}", value=alert_value, inline=False)

        
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))
<<<<<<< HEAD
        """
=======
>>>>>>> 8625a649efdad5e4e855ffba42f9e408769b9bf6

    
    #nightwave
    @app_commands.command(name="nightwave", description="Send current nightwave.")
    async def nightwave(self, interaction: discord.Interaction, challenge: bool = False):
        nightwavejson = await self.getWarframeData("nightwave")
        if nightwavejson == None:
            await interaction.response.send_message("Something went wrong.")
            return

        embed = discord.Embed(title="Current Nightwave")
        embed.add_field(name="Name", value=nightwavejson["tag"])
        start_timestamp = self.convertTimestamp(nightwavejson["activation"])
        embed.add_field(name="Started", value= f"<t:{int(start_timestamp)}:R>")
        expiry_timestamp = self.convertTimestamp(nightwavejson["expiry"])
        embed.add_field(name="Ends", value=f"<t:{int(expiry_timestamp)}:R>")

        if challenge:
            for i in range(len(nightwavejson["activeChallenges"])):
                challenge_value = (
                    f"{nightwavejson['activeChallenges'][i]['title']} - "
                    f"{nightwavejson['activeChallenges'][i]['desc']} - "
                    f"{nightwavejson['activeChallenges'][i]['reputation']}"
                )
                embed.add_field(name=f"Challenge {i + 1}", value=challenge_value, inline=False)

       
        
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))


    #random
    @app_commands.command(name="random", description="Send random warframe/weapon name.")
    async def random(self, interaction:discord.Interaction, category: str):
        try:
            if category == "warframe":
                data = await self.getWarframeDataGithub("Warframes")
            elif category == "primary":
                data = await self.getWarframeDataGithub("Primary")
            elif category == "secondary":
                data = await self.getWarframeDataGithub("Secondary")
            elif category == "melee":
                data = await self.getWarframeDataGithub("Melee")
            elif category == "kuva":
                data = await self.getKuvaTenet("Kuva")
            elif category == "tenet":
                data = await self.getKuvaTenet("Tenet")
            else:
                embed = discord.Embed(title="Invalid Category", description="Please select a valid category: warframe, primary, secondary, melee, kuva and tenet.")
                await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))
                return
        except Exception as e:
            print(f"Failed to get the data: {e}")
            await interaction.response.send_message("Something went wrong.")
            return

        if data == None:
            await interaction.response.send_message("Something went wrong.")
            return
        randomjson = random.choice(data)
        random_name = randomjson["name"]
        image = self.getImageLink(randomjson["imageName"])
        embed = discord.Embed(title=f"Random {category.capitalize()}", description=f"[{random_name}]({randomjson['wikiaUrl']})")
        embed.set_thumbnail(url=image)
        try:
            embed.add_field(name="Vaulted", value=randomjson["vaulted"])
        except:
            pass
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))
        
    #events
    @app_commands.command(name="events", description="Send current events.")
    async def events(self, interaction:discord.Interaction):
        try:
            eventjson = await self.getWarframeData("events")
            if eventjson == None:
                await interaction.response.send_message("Something went wrong.")
                return

            embed = discord.Embed(title="Current Events")
            for i in range(len(eventjson)):
                expiry_timestamp = self.convertTimestamp(eventjson[i]["expiry"])
                started_timestamp = self.convertTimestamp(eventjson[i]["activation"])
                event_value = (
                    (f"\n{eventjson[i]['tooltip']}" if 'tooltip' in eventjson[i] else '') +
                    f"\nStarted: <t:{int(started_timestamp)}:R>"
                    f"\nExpiry: <t:{int(expiry_timestamp)}:R>" 
                )
                embed.add_field(name=f"{eventjson[i]['description']}", value=event_value, inline=False)

            await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))

        except Exception as e:
            print(e)
            await interaction.response.send_message("Something went wrong.")

    #dailyReset shows the time of daily reset
    @app_commands.command(name="daily", description="Send the time of daily reset.")
    async def dailyReset(self, interaction: discord.Interaction):
        try:
            now = datetime.utcnow()
            # for daily reset of 0:00 UTC
            reset0 = datetime(now.year, now.month, now.day, 0, 0, 0)
            if now.hour >= 0:
                reset0 += timedelta(days=1)

            # for daily reset of 17:00 UTC
            reset17 = datetime(now.year, now.month, now.day, 17, 0, 0)
            if now.hour >= 17:
                reset17 += timedelta(days=1)

            embed = discord.Embed(title="Daily Reset")
            embed.add_field(name="For Daily Tribute, Nightwave, Steel Path, Syndicate Standing, Focus, Trades, Argon, Acrithis", value=f"<t:{int(reset0.timestamp())}:R>", inline=False)
            embed.add_field(name="For Sortie, Syndicate Alerts", value=f"<t:{int(reset17.timestamp())}:R>", inline=False)
            await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions(users=[interaction.user]))
        except Exception as e:
            print(e)
            await interaction.response.send_message("Something went wrong!")
        



async def setup(bot):
    await bot.add_cog(WarframeCog(bot))



    