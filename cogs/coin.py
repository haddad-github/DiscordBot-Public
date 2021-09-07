import json
from bs4 import BeautifulSoup
import discord
import requests
from discord.ext import commands


class coin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def coin(self, ctx, coin):

        url = 'https://api.livecoinwatch.com/coins/single'
        api_key = '###'

        params = {
            'currency': 'USD',
            'code': coin.upper(),
            'meta': True
        }

        headers = {

            'x-api-key': api_key,
            'Content-Type': 'application/json'

        }

        response = requests.post(url, data=json.dumps(params), headers=headers)

        data = json.loads(response.text)

        name = data['name']
        icon = data['png64']
        rate = data['rate']

        if rate > 1:
            rate = round(rate, 2)

        if rate < 1:
            rate = round(rate, 8)

        price = f'$ {rate:,}'

        HEADERS = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
        }

        url2 = f'https://www.livecoinwatch.com/price/{name}-{coin.upper()}'
        response2 = requests.get(url2, headers=HEADERS)
        soup = BeautifulSoup(response2.content, "html.parser")

        neg = False
        h24change = soup.find_all(class_='col-lg-3 col-xl-2 px-0 py-1 py-md-0')[1].find(class_='cion-item px-1 grow')

        if h24change == None:
            h24change = soup.find_all(class_='col-lg-3 col-xl-2 px-0 py-1 py-md-0')[1].find(class_='cion-item px-1 fall')
            neg = True

        h24change = h24change.find(class_='percent d-none d-lg-block').text

        if neg == False:
            h24change = f'+{h24change}'

        elif neg == True:
            h24change = f'-{h24change}'

        h24change = soup.find(class_='percent d-none d-lg-block').text

        embed = discord.Embed(title="[Coin] " + f'{name} ({coin})')
        embed.add_field(name= "USD", value=price)
        embed.add_field(name="Daily change", value=f'(**{h24change}**)')
        embed.set_thumbnail(url=icon)

        await ctx.channel.send(embed=embed)

        # api_key = '09f7e451-b941-45a7-a063-68de9ae25dfb'
        #
        # url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        #
        # coin = coin.lower()
        #
        # if coin == 'bitcoin':
        #     coin = 'btc'
        #
        # if coin == 'etherum' or coin == 'ethereum' or coin == 'etherium':
        #     coin = 'eth'
        #
        # if coin == 'shiba':
        #     coin = 'shib'
        #
        # if coin == 'dogecoin':
        #     coin = 'doge'
        #
        # headers = {
        #     'X-CMC_PRO_API_KEY': api_key,
        #     'Accepts': 'application/json'
        # }
        #
        # parameters = {
        #
        #     'symbol': coin,
        #     'convert': 'USD'
        #
        # }
        #
        # session = Session()
        # session.headers.update(headers)
        #
        # response = session.get(url, params=parameters)
        # data = json.loads(response.text)
        #
        # for i in data['data'].keys():
        #     n = i
        #
        # name = data['data'][n]['name']
        # symbol = data['data'][n]['symbol']
        # p = Decimal(data['data'][n]['quote']['USD']['price'])
        # if p < 1:
        #     p = round(Decimal(p), 8)
        # else:
        #     p = round(p, 2)
        # price = f'$ {p:,}'
        # c = data['data'][n]['quote']['USD']['percent_change_24h']
        # change24h = f'{round(c, 2)} %'
        #
        # ##
        #
        # name_traits = name.replace(" ", "-")
        # url2 = 'https://coinmarketcap.com/currencies/' + name_traits
        #
        # req = requests.get(url2)
        # bs = soup(req.text, 'html.parser')
        #
        # icon_class = bs.find(class_='sc-16r8icm-0 gpRPnR nameHeader___27HU_')
        # elems = []
        #
        # for i in icon_class:
        #     elems.append(i.get('src'))
        #
        # icon_url = elems[0]
        #
        # if "-" not in change24h:
        #     change24h = f'+{change24h}'
        # ##
        #
        # embed = discord.Embed(title="[Coin] " + f'{name} ({symbol})')
        # embed.add_field(name= "USD", value=price)
        # embed.add_field(name="Daily change", value=f'(**{change24h}**)')
        # embed.set_thumbnail(url=icon_url)
        #
        # await ctx.channel.send(embed=embed)

    ###################################################################################

def setup(client):
    client.add_cog(coin(client))



