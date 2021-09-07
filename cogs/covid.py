from discord.ext import commands
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re

class covid(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def covid(self, ctx):
        url = "https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec"

        # Read page
        uClient = uReq(url)
        page_html = uClient.read()

        # Parse HTML
        page_soup = soup(page_html, "html.parser")

        # Find the class where the word's definition is found in and print it with ".text" to remove all the <p>'s, etc.
        text = page_soup.find_all(class_="ce-bodytext")

        cas = re.findall(".*show:</p><ul><li>(.*) bringing.*", str(text[2]))

        death = re.findall(".*deaths: 	<ul><li>(.*)intensive care.*", str(text[2]))

        death_last = re.findall("\['(.*)in the last 24.*", str(death))
        death_last_final = death_last[0].replace("\\xa0", " ")

        hospital = re.findall(".*,</li></ul></li><li>(.*)hospitalizations.*", str(death))
        hospital_2 = hospital[0]
        hospital_2 = hospital_2.replace("\\xa0", "")

        await ctx.channel.send(
            "```Last 24 hours, country of Quebec (merci): \n\n• {}\n• {}\n• {} hospitalizations```".format(
                cas[0].replace(",", ""), death_last_final, hospital_2))


    ###################################################################################

def setup(client):
    client.add_cog(covid(client))
