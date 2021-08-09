from discord.ext import commands
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re


class table(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################


    async def table(self, ctx, league):

        if league == "england":
            url = "https://www.skysports.com/premier-league-table"
            url_1 = "https://www.espn.com/soccer/standings/_/league/eng.1"

        elif league == "spain":
            url = "https://www.skysports.com/la-liga-table"
            url_1 = "https://www.espn.com/soccer/standings/_/league/esp.1"

        elif league == "italy":
            url = "https://www.skysports.com/serie-a-table"
            url_1 = "https://www.espn.com/soccer/standings/_/league/ita.1"

        elif league == "germany":
            url = "https://www.skysports.com/bundesliga-table"
            url_1 = "https://www.espn.com/soccer/standings/_/league/ger.1"

        elif league == "france":
            url = "https://www.skysports.com/ligue-1-table"
            url_1 = "https://www.espn.com/soccer/standings/_/league/fra.1"

        else:
            await ctx.channel.send("Enter a valid league")

        uClient = uReq(url)
        page_html = uClient.read()
        page_soup = soup(page_html, "html.parser")

        uClient_1 = uReq(url_1)
        page_html_1 = uClient_1.read()
        page_soup_1 = soup(page_html_1, "html.parser")

        teams = page_soup.find_all(class_="standing-table__cell--name-link")
        points = page_soup_1.find_all(class_="stat-cell")

        points_text = points[7::8]
        team_names = []  #Creates the team name holding list referenced in print statement

        table_string = ""

        n = 0
        for i in points_text:
            n += 1
            for team in teams:
                points_text_string = str(i)
                points_clean = re.findall(r'\d+', points_text_string)
                result = "".join(points_clean)
                team_names.append(team.text)  #Adds the team name to the team names list

                un = str(n) + ". " + team_names[n - 1]
                deux = result

            table = f"{un:<30} {deux} \n"

            table_string += table

        await ctx.channel.send("```#    Team                    Points\n───────────────────────────────────\n{}```".format(table_string))


    ###################################################################################

def setup(client):
    client.add_cog(table(client))
