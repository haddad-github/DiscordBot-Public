from discord.ext import commands
import re
import random
import requests
import lxml.html
import time

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import yfinance as yf

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
async def anime(ctx,*, anime):
    url = "https://myanimelist.net/anime.php?cat=anime&q=" + anime

    # Read page
    uClient = uReq(url)
    page_html = uClient.read()

    # Parse HTML
    page_soup = soup(page_html, "html.parser")

    # Find the class where the word's definition is found in and print it with ".text" to remove all the <p>'s, etc.
    tds = page_soup.find_all(class_="borderClass ac bgColor0")

    nom = page_soup.find_all(class_="borderClass bgColor0")
    nom_re = re.findall(".*<img alt=(.*) border=\"0\".*", str(nom[0]))

    # Append the values of the td's, then pick the one of the first anime that pops ups (values[2])
    values = []
    for td in tds:
        values.append(td.text)

    rating = values[2].split()[0] #[2] inclut les espaces; donc split() pour mettre en liste, puis [0] pour 1ier elem

    await ctx.channel.send("```[Anime rating] {}: {}```".format(nom_re[0].split("\"")[1],rating))

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

#Stock using yfinance
@client.command()
async def stock(ctx, ticker):

    stock = yf.Ticker(ticker)
    
    pourcent = round((1 - (stock.info["ask"]/stock.info["previousClose"]))*100, 2)

    if stock.info["quoteType"] == "ETF":
        price = "$ {}".format(round(stock.info["ask"], 2))

        if stock.info["ask"] >= stock.info["previousClose"]:
            ratio = "+{} %".format(pourcent)
        else:
            ratio = "-{} %".format(pourcent)

    else:
        price = "$ {}".format(round(stock.info["currentPrice"], 2))

        if stock.info["currentPrice"] >= stock.info["previousClose"]:
            ratio = "+{} %".format(stock.info["currentRatio"])
        else:
            ratio = "-{} %".format(stock.info["currentRatio"])


    name = stock.info["shortName"]
    day_high = "$ {}".format(round(stock.info["dayHigh"],2))
    openN = "$ {}".format(round(stock.info["open"], 2))
    prev_close = "$ {}".format(round(stock.info["previousClose"],2))
    volumeN = stock.info["volume"]
    average_volumeN = stock.info["averageVolume"]

    volume = f"{volumeN:,}"
    average_volume = f"{average_volumeN:,}"


    await ctx.channel.send("[Stock] **{}**\n```Price: {}\nDaily change: {}\n\nHigh of the day: {}\nOpen: {}\nPrevious close: {}\n\n"
      "Volume: {}\nAvg. Volume: {}```".format(name, price, ratio, day_high, openN, prev_close, volume, average_volume))


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

    html = requests.get("https://store.steampowered.com/search/?term=" + game +"&category1=998")
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

#Gets meteo for 2 places only (expansion possible if ever relevant) from weather.gc.ca
#Currently buggy before a certain hour ET due to index changes throughout the day
@client.command()
async def meteo(ctx, region):

    if region == "laval".lower():
        num = "76"
    elif region == "mtl".lower():
        num = "147"

    else:
        await ctx.channel.send("Region irrelevant, choisi Laval ou Mtl, merci")

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    }

    result = requests.get("https://weather.gc.ca/city/pages/qc-{}_metric_e.html".format(num), headers=HEADERS)
    soup_a = soup(result.content, "html.parser")

    row = soup_a.find_all(class_="div-column")
    row_str = str(row)

    days = re.findall(".*\">(.*)</strong>.*", row_str)

    temps_day = re.findall(".*title=\"max\">(.*)<abbr title=\"Celsius\".*", row_str)

    predictions_night = re.findall(".*img alt=\"(.*)\" class.*", row_str)[0::2]

    temps_night = re.findall(".*title=\"min\">(.*)<abbr title=\"Celsius\".*", row_str)

    predictions_day = re.findall(".*img alt=\"(.*)\" class.*", row_str)[1::2]

    predictions_night.append("N/A")
    temps_night.append("N/A")

    for i, word in enumerate(temps_night):
        if word == "N/A":
            temps_night[i] = ":question:"

    for i, word in enumerate(predictions_day):
        if word == "Mainly cloudy" or word == "Partly cloudy":
            predictions_day[i] = ":cloud:"

        elif word == "Sunny" or word == "Clear":
            predictions_day[i] = ":sunny:"

        elif word == "Chance of showers" or word == "Periods of rain":
            predictions_day[i] = ":cloud_rain:"

    for i, word in enumerate(predictions_night):
        if word == "Mainly cloudy" or word == "Partly cloudy":
            predictions_night[i] = ":cloud:"

        elif word == "Sunny" or word == "Clear":
            predictions_night[i] = ":sunny:"

        elif word == "Chance of showers" or word == "Periods of rain":
            predictions_night[i] = ":cloud_rain:"

        elif word == "N/A":
            predictions_night[i] = ":question:"


    semaine = ""

    for i in range(len(days)):

        semaine += "{}\n───\n :sun_with_face: :  *{}*    *{}*\n :crescent_moon: :  *{}*    *{}*\n\n".format(days[i], temps_day[i], predictions_day[i],
                                                                        temps_night[i+1], predictions_night[i+1])

    await ctx.channel.send(" {} ".format(semaine))

#OSRS G.E. Price
@client.command()
async def ge(ctx,*,item):

    html = requests.get("https://oldschool.runescape.wiki/w/" + item)
    doc = lxml.html.fromstring(html.content)

    name = doc.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr[1]/th/text()')
    price = doc.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr[29]/td/span/span/text()')

    if price == []:
        price = doc.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr[28]/td/span/span/text()')

    name_str = "".join(name)

    price_str = "".join(price)

    await ctx.channel.send("```{}: {} gp```".format(name_str, price_str))

#Parc available
@client.command()
async def foot(ctx, parc):

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Locate chromedriver et utiliser chrome
    path = "/usr/bin/chromedriver"
    driver = webdriver.Chrome(path, options=chrome_options)

    if parc == "cartier":
        driver.get("https://www.publicationsports.com/cal/index.php?o=36&t=212&p=516&lg=fr")

    elif parc == "coursol":
        driver.get("https://www.publicationsports.com/cal/index.php?o=36&t=192&p=536&lg=fr")

    days = driver.find_elements_by_class_name("fc-col-header-cell-cushion ")

    d = []
    e = []
    ts = []

    d.append(days[0].text)

    events = driver.find_elements_by_class_name("fc-event-title-container")

    for event in events:
        e.append(event.text)

    times = driver.find_elements_by_class_name("fc-event-time")

    for time in times:
        ts.append(time.text)

    for i, t in enumerate(ts):
        if "00:00" in t:
            ts = ts[:i]

    zipped = sorted(zip(e, ts))

    event_and_time = ""

    for e, ts in zipped:
        event_and_time += str(e) + " " + "\n"
        event_and_time += str(ts) + " " + "\n" + "\n"

    if zipped == []:
        await ctx.channel.send("```{}\n\nLibre```".format(d[0].upper()))
    else:
        await ctx.channel.send("```{}\n\n{}```".format(d[0].upper(), event_and_time))


#Covid Quebec 24 hours
#Currently buggy due to indexation issues on different days
@client.command()
async def covid(ctx):
    url = "https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec"

    # Read page
    uClient = uReq(url)
    page_html = uClient.read()

    # Parse HTML
    page_soup = soup(page_html, "html.parser")

    # Find the class where the word's definition is found in and print it with ".text" to remove all the <p>'s, etc.
    text = page_soup.find_all(class_="ce-bodytext")

    # print(str(text[2]))

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

#Flip coins
@client.command()
async def flip(ctx):

    choix = ("Pile", "Face")
    coin = random.choice(choix)

    await ctx.channel.send(coin)

#All commands
@client.command()
async def commands(ctx):

    await ctx.channel.send("```[OFF]!remove [mot] pour delete tous les messages contenant ce mot dans l'histoire du channel\n"
                           "\n!et [mot] pour avoir l'etymologie d'un mot (ex: !et bird)\n"
                           "\n!anime [nom anime] pour avoir le rating d'un anime (ex: !anime bleach)\n"
                           "\n!coin [nom du crypto] pour avoir le prix et 24h change du coin\n"
                           "\n!stock [NASDAQ code] pour avoir le prix et 24h change du stock\n"
                           "\n!gas [region] pour avoir le prix moyen aujourd'hui\n"
                           "\n!foot [parc] pour avoir la disponibilitee du parc aujourd'hui\n"
                           "\n!table [england/spain/italy/germany] pour avoir la table de la ligue en ce momment\n"
                           "\n!steam [nom du jeu] pour avoir le prix du jeu sur Steam ou pour savoir si c'est en rabais\n"
                           "\n!ge [item] pour avoir le prix d'un item de OSRS\n"
                           "\n!foot [parc] pour avoir disponibilitee du parc"
                           "\n[BUG]!meteo [laval/mtl] pour avoir la meteo des 7 prochains jours\n"
                           "\n!flip pour flip un cous (pile ou face)\n```")

#Must be the last line of code
client.run("BOT TOKEN HERE") #runs the client by using bot's token
