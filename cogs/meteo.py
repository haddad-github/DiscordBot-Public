import discord
from discord.ext import commands
import requests

class meteo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def weather(self, ctx):

        api_key = "###"

        lon = ###
        lat = ###
        part = "minute,hourly"

        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}'

        response = requests.get(url).json()

        days = []
        days_feel = []

        nights = []
        nights_feel = []

        descr = []

        for i in response['daily']:
            descr.append(i['weather'][0]['main'] + " (" + i['weather'][0]['description'] + ")")

            days_feel.append(round(i['feels_like']['day'] - 273.15))
            nights_feel.append(round(i['feels_like']['night'] - 273.15))
            days.append(round(i['temp']['day'] - 273.15))
            nights.append(round(i['temp']['night'] - 273.15))

        string = ""
        for i in range(len(days)):
            if i == 0:
                string += f"\n**Day {i + 1} (Today)**\n"
            elif i == 1:
                string += f"**\nDay {i + 1} (Tomorrow)**\n"
            else:
                string += f"**\nDay {i + 1}**\n"
            string += "Morning: " + str(days[i]) + "°C" + " ; Feels like: " + str(days_feel[i]) + "°C\n"
            string += "Night: " + str(nights[i]) + "°C" + " ; Feels like: " + str(nights_feel[i]) + "°C\n"
            string += "Conditions: " + descr[i] + "\n"


        embed = discord.Embed(title="Laval, QC - 8 days weather forecast")

        embed.add_field(name="_" ,value=string)

        await ctx.channel.send(embed = embed)


    ###################################################################################

def setup(client):
    client.add_cog(meteo(client))
