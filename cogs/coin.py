import discord
from discord.ext import commands
from decimal import Decimal
from bs4 import BeautifulSoup as soup
import requests
from requests import Session
import json

class coin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def coin(self, ctx, coin):

        api_key = '####'

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

        coin = coin.lower()

        if coin == 'bitcoin':
            coin = 'btc'

        if coin == 'etherum' or coin == 'ethereum' or coin == 'etherium':
            coin = 'eth'

        if coin == 'shiba':
            coin = 'shib'

        if coin == 'dogecoin':
            coin = 'doge'

        headers = {
            'X-CMC_PRO_API_KEY': api_key,
            'Accepts': 'application/json'
        }

        parameters = {

            'symbol': coin,
            'convert': 'USD'

        }

        session = Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        for i in data['data'].keys():
            n = i

        name = data['data'][n]['name']
        symbol = data['data'][n]['symbol']
        p = Decimal(data['data'][n]['quote']['USD']['price'])
        if p < 1:
            p = round(Decimal(p), 8)
        else:
            p = round(p, 2)
        price = f'$ {p:,}'
        c = data['data'][n]['quote']['USD']['percent_change_24h']
        change24h = f'{round(c, 2)} %'

        ##

        name_traits = name.replace(" ", "-")
        url2 = 'https://coinmarketcap.com/currencies/' + name_traits

        req = requests.get(url2)
        bs = soup(req.text, 'html.parser')

        icon_class = bs.find(class_='sc-16r8icm-0 gpRPnR nameHeader___27HU_')
        elems = []

        for i in icon_class:
            elems.append(i.get('src'))

        icon_url = elems[0]

        if "-" not in change24h:
            change24h = f'+{change24h}'
        ##

        embed = discord.Embed(title="[Coin] " + f'{name} ({symbol})')
        embed.add_field(name= "USD", value=price)
        embed.add_field(name="Daily change", value=f'(**{change24h}**)')
        embed.set_thumbnail(url=icon_url)

        await ctx.channel.send(embed=embed)

    ###################################################################################

def setup(client):
    client.add_cog(coin(client))



