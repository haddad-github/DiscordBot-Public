from discord.ext import commands
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

class et(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()


    ###################################################################################

    async def et(self, ctx, word):

        url = "https://www.etymonline.com/search?q=" + word
        uClient = uReq(url)
        page_html = uClient.read()
        page_soup = soup(page_html, "html.parser")

        definition = page_soup.find(class_="word__defination--2q7ZH undefined").text

        await ctx.channel.send("[Etymology] **{}**```{}```".format(word.upper(), definition))

    ###################################################################################


def setup(client):
    client.add_cog(et(client))