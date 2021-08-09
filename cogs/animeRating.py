import discord
from discord.ext import commands
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

class anime(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def anime(self, ctx,*, anime):

        animeG = anime.replace(" ", "+")

        anime = anime.replace(" ", "_")

        url = "https://myanimelist.net/anime.php?cat=anime&q=" + anime

        #Read page
        uClient = uReq(url)
        page_html = uClient.read()

        #Parse HTML
        page_soup = soup(page_html, "html.parser")

        name = page_soup.find(class_="hoverinfo_trigger fw-b fl-l").text

        link = page_soup.find(class_="hoverinfo_trigger").get('href')

        pic = page_soup.find(class_="picSurround")
        img = pic.find('img').attrs['data-src']

        all_stats = page_soup.find_all(class_="borderClass ac bgColor0")

        stats = []
        for i in all_stats[0:3]:
            stats.append(i.text.strip())

        type = stats[0]
        eps = stats[1]
        rating = stats[2]

        if eps == "-":
            eps = "On going"

        embed = discord.Embed(title=name)
        embed.set_thumbnail(url=img)
        if eps == "On going":
            embed.add_field(name="Description", value=f'{type}: {eps}\nRating: **{rating}**\n')
        else:
            embed.add_field(name="Description", value=f'{type}: {eps} episodes\nRating: **{rating}**\n')
        embed.add_field(name="MyAnimeList:", value=link)
        embed.add_field(name="Watch here:", value=f'https://animekisa.tv/search?q={animeG}')

        await ctx.channel.send(embed=embed)

        ###################################################################################


def setup(client):
    client.add_cog(anime(client))