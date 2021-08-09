from discord.ext import commands
import requests
import lxml.html

class steam(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def steam(self, ctx, game):

        html = requests.get("https://store.steampowered.com/search/?term=" + game + "&category1=998")
        doc = lxml.html.fromstring(html.content)

        title = doc.xpath('//*[@id="search_resultsRows"]/a[1]/div[2]/div[1]/span/text()')[0]
        discount = doc.xpath('.//div[@class="col search_discount  responsive_secondrow"]/text()')

        if not discount:
            discount = "Pas de rabais"
            price = doc.xpath('.//div[@class="col search_price  responsive_secondrow"]/text()')
        else:
            price = doc.xpath('.//div[@class="col search_price discounted responsive_secondrow"]/text()')

        price_split = price[0].split()
        price_final = " ".join(price_split)

        await ctx.channel.send("```{}: {} ({})```".format(title, price_final, discount))

    ###################################################################################

def setup(client):
    client.add_cog(steam(client))
