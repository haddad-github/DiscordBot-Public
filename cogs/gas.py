import discord
from discord.ext import commands
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


class gas(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def gas(self, ctx, region):
        url = "###" + region
        uClient = uReq(url)
        page_html = uClient.read()
        page_soup = soup(page_html, "html.parser")
        textprix = page_soup.find(class_="graphic-column-text-price").text
        textprix_seul_no_decimal = float(textprix[1:4:])
        textprix_restant = float(textprix[5])
        textprix_restant_vrai = textprix_restant / 10

        prix_final = textprix_seul_no_decimal + textprix_restant_vrai

        embed = discord.Embed(title=f'Prix d\'essence moyen à {region.upper()}:\n')
        embed.add_field(name= "Ordinaire", value=prix_final)
        embed.add_field(name="Extra", value=prix_final+15)
        embed.add_field(name="Supreme", value=prix_final+18)

        await ctx.channel.send(embed=embed)

    ###################################################################################

def setup(client):
    client.add_cog(gas(client))
