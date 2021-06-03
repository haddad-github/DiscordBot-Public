from discord.ext import commands
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re
import random
import requests
import lxml.html


#"!" becomes the prefix for all commands (ex: !ping)
client = commands.Bot(command_prefix = "!")

#Indicates if bot is active
@client.event #event ([variable].event)
async def on_ready():
    print("Bot is ready.")


#ctx = channel where it's being called
#!remove [word]
#removes all instances of that word
#Counts number of messages deleted; starts count at n = -1 car command itself counts
@client.command()
@commands.has_permissions(administrator=True)
async def remove(ctx, word):
    n = -1
    async for message in ctx.channel.history(): #optional limit ; .history(limit=integer)
        if word in message.content.lower(): #recognizes word regardless of version (ex: bonjour = bOnJoUr)
            await message.delete()

        if message.content.find(word) != -1:
            n += 1

    await ctx.channel.send("J'ai delete {} instance(s) du mot".format(n)) #n = number of deleted messages

#___________________________________________________________________________
#Notes:
#Works with spoiler words too

#!remove [space] and !remove [ALT+255] does not remove messages; good
############################################################################

#Gives word's etymology based on etymonline
@client.command()
async def et(ctx, word):
    url = "https://www.etymonline.com/search?q=" + word
    uClient = uReq(url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    definition = page_soup.find(class_="word__defination--2q7ZH undefined").text

    await ctx.channel.send("[Etymology] **{}**```{}```".format(word.upper(), definition))

#Gives anime's rating based on myanimelist
@client.command()
async def anime(ctx, anime):
    url = "https://myanimelist.net/anime.php?cat=anime&q=" + anime
    uClient = uReq(url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    tds = page_soup.find_all(class_="borderClass ac bgColor0")

    values = []
    for td in tds:
        values.append(td.text)

    rating = values[2].split()[0] #[2] inclut les espaces; donc split() pour mettre en liste, puis [0] pour 1ier elem

    await ctx.channel.send("[Anime rating] **{}**: {}".format(anime.upper(),rating))

#Gives cryptocurrency price based on coindesk
@client.command()
async def coin(ctx, coin):

    url = "https://www.coindesk.com/price/"+coin
    uClient = uReq(url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    price = page_soup.find(class_="price-large").text
    percent = page_soup.find(class_="percent-value-text").text

    await ctx.channel.send("[Coin] **{}**\n"
                           "```Price: {}\n"
                           "Daily change: {}%```"
                           .format(coin.upper(), price,percent))

#Gives stock price based on yahoo finance
@client.command()
async def stock(ctx, stock):

    url = "https://finance.yahoo.com/quote/" + stock
    uClient = uReq(url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")

    price = page_soup.find(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)").text
    percent_non_text = page_soup.find(class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)")

    if percent_non_text == None:
        percent = page_soup.find(class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)").text

    else:
        percent = page_soup.find(class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)").text

    print(price)
    print(percent)

    await ctx.channel.send("[Stock] **{}**\n"
                           "```Price: ${}\n"
                           "Daily change: {}```"
                           .format(stock.upper(), price, percent))

#Gives gas price based on CAAQuebec
@client.command()
async def gas(ctx, region):

    url = "https://www.caaquebec.com/en/on-the-road/public-interest/gasoline-matters/gasoline-watch/region/"+region
    uClient = uReq(url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")
    textprix = page_soup.find(class_="graphic-column-text-price").text
    textprix_seul_no_decimal = float(textprix[1:4:])
    textprix_restant = float(textprix[5])
    textprix_restant_vrai = textprix_restant / 10

    prix_final = textprix_seul_no_decimal + textprix_restant_vrai

    await ctx.channel.send("```Prix d'essence moyen à {}:\n"
                           "Ordinaire: {}\n"
                           "Extra: {}\n"
                           "Supreme: {}\n```".format(region, prix_final, prix_final+15, prix_final+18))

#Gives football league table based on Skysports and ESPN
@client.command()
async def table(ctx, league):

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
        await ctx.channel.send("Enter ")

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

#Gives Steam game's price and discount
@client.command()
async def steam(ctx, game):

    html = requests.get("https://store.steampowered.com/search/?term=" + game)
    doc = lxml.html.fromstring(html.content)

    title = doc.xpath('//*[@id="search_resultsRows"]/a[1]/div[2]/div[1]/span/text()')[0]
    discount = doc.xpath('.//div[@class="col search_discount  responsive_secondrow"]/text()')

    price = doc.xpath('.//div[@class="col search_price  responsive_secondrow"]/text()')
    price_split = price[0].split()
    price_final = " ".join(price_split)

    if not discount:
        discount = "Pas de rabais"


    await ctx.channel.send("```{}: {} ({})```".format(title, price_final, discount))


#Flip coins
@client.command()
async def flip(ctx):

    choix = ("Pile", "Face")
    coin = random.choice(choix)

    await ctx.channel.send(coin)

#All commands
@client.command()
async def commands(ctx):

    await ctx.channel.send("```!remove [mot] pour delete tous les messages contenant ce mot dans l'histoire du channel\n"
                           "\n!et [mot] pour avoir l'etymologie d'un mot (ex: !et bird)\n"
                           "\n!anime [nom anime] pour avoir le rating d'un anime (ex: !anime bleach)\n"
                           "\n!coin [nom du crypto] pour avoir le prix et 24h change du coin\n"
                           "\n!stock [NASDAQ code] pour avoir le prix et 24h change du stock\n"
                           "\n!gas [region] pour avoir le prix moyen aujourd'hui\n"
                           "\n!table [england/spain/italy/germany] pour avoir la table de la ligue en ce momment\n"
                           "\n!steam [nom du jeu] pour avoir le prix du jeu sur Steam ou pour savoir si c'est en rabais"
                           "\n!flip pour flip un cous (pile ou face)\n```")

#Must be the last line of code
client.run("BOT TOKEN HERE") #runs the client by using bot's token