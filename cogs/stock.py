import discord
from discord.ext import commands
import yfinance as yf

class stock(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def stock(self, ctx, ticker):

        stock = yf.Ticker(ticker)

        logo = stock.info['logo_url']

        if stock.info["quoteType"] == "ETF":
            price = "$ {}".format(round(stock.info["ask"], 2))
            pourcent = abs(round((1 - (stock.info["ask"] / stock.info["previousClose"])) * 100, 2))

            if stock.info["ask"] >= stock.info["previousClose"]:
                ratio = "+{} %".format(pourcent)
            else:
                ratio = "-{} %".format(pourcent)

        else:
            price = "$ {}".format(round(stock.info["currentPrice"], 2))
            pourcent_stock = abs(round((1 - (stock.info["currentPrice"] / stock.info["previousClose"])) * 100, 2))

            if stock.info["currentPrice"] >= stock.info["previousClose"]:
                ratio = "+{} %".format(pourcent_stock)
            else:
                ratio = "-{} %".format(pourcent_stock)

        name = stock.info["shortName"]
        day_high = "$ {}".format(round(stock.info["dayHigh"], 2))
        openN = "$ {}".format(round(stock.info["open"], 2))
        prev_close = "$ {}".format(round(stock.info["previousClose"], 2))
        volumeN = stock.info["volume"]
        average_volumeN = stock.info["averageVolume"]

        volume = f"{volumeN:,}"
        average_volume = f"{average_volumeN:,}"

        embed = discord.Embed(title="[Stock] " + name)
        embed.set_thumbnail(url=logo)
        embed.add_field(name="Price: ", value=price)
        embed.add_field(name="Daily change: ", value=f'(**{ratio}**)')
        embed.add_field(name="High of the day: ", value=day_high)
        embed.add_field(name="Open: ", value=openN)
        embed.add_field(name="Previous close: ", value=prev_close)
        embed.add_field(name="Volume: ", value=volume)
        #embed.add_field(name="Avg. Volume: ", value=average_volume)


        await ctx.channel.send(embed=embed)

        #await ctx.channel.send(
        #    "[Stock] **{}**\n```Price: {}\nDaily change: {}\n\nHigh of the day: {}\nOpen: {}\nPrevious close: {}\n\n"
        #    "Volume: {}\nAvg. Volume: {}```".format(name, price, ratio, day_high, openN, prev_close, volume,
        #                                            average_volume))

        ###################################################################################

def setup(client):
    client.add_cog(stock(client))

# Gives stock price based on yahoo finance
# @client.command()
# async def stock(ctx, stock):

#    url = "https://finance.yahoo.com/quote/" + stock
#    uClient = uReq(url)
#    page_html = uClient.read()
#    page_soup = soup(page_html, "html.parser")

#    price = page_soup.find(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)").text
#    percent_non_text = page_soup.find(class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)")

#    if percent_non_text == None:
#        percent = page_soup.find(class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)").text

#    else:
#        percent = page_soup.find(class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)").text

#    print(price)
#    print(percent)

#    await ctx.channel.send("[Stock] **{}**\n"
#                           "```Price: ${}\n"
#                           "Daily change: {}```"
#                           .format(stock.upper(), price, percent))

# Stock using selenium
# @client.command()
# async def stock(ctx, stock):

#    chrome_options = Options()
#    chrome_options.add_argument("--headless")

#    path = "C:\chromedriver.exe"
#    driver = webdriver.Chrome(path, options=chrome_options)

#    driver.get("https://finance.yahoo.com/quote/"+stock)

#    name = driver.find_element_by_xpath("//*[@id=\"quote-header-info\"]/div[2]/div[1]/div[1]/h1").text
#    price = driver.find_element_by_xpath("//*[@id=\"quote-header-info\"]/div[3]/div[1]/div/span[1]").text
#    percent = driver.find_element_by_xpath("//*[@id=\"quote-header-info\"]/div[3]/div[1]/div/span[2]").text

#    driver.quit()

#    sign = re.search(r'\((.*?)\)', name).group(0)

#    await ctx.channel.send("[Stock]: {}**{}**\n```Price: $ {}\nDaily change: {}```".format(name.split(sign)[0], sign, price, percent))