import discord
from discord.ext import commands
from bs4 import BeautifulSoup as soup
import requests

class ge(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def ge(self, ctx, *, item):

        item = item.replace(" ", "_")

        url = 'https://oldschool.runescape.wiki/w/' + item
        html = requests.get(url)
        bs = soup(html.text, 'html.parser')
        real = bs.find(class_="realtimePrices")
        id = real.get('data-itemid')

        # Get info from json
        url2 = 'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=' + id
        req2 = requests.get(url2)
        data = req2.json()
        data_item = data['item']
        print(data_item)

        name = data_item['name']
        icon = data_item['icon']
        price = data_item['current']['price']
        today = data_item['today']['price']
        day30 = data_item['day30']['change']
        day90 = data_item['day90']['change']
        day180 = data_item['day180']['change']

        embed = discord.Embed(title=name)
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Price", value=f'{price} gp')
        embed.add_field(name="Today", value=f'{today} gp')
        embed.add_field(name="30 day / 90 day / 180 day", value=f'{day30} / {day90} / {day180}')

        await ctx.channel.send(embed=embed)


    ###################################################################################

def setup(client):
    client.add_cog(ge(client))
