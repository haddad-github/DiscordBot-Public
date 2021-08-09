from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class aoe(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def aoe(self, ctx, civ):

        all_civs = ["aztecs", "berbers", "britons", "bulgarians", "burgundians", "burmese", "byzantines", "celts",
                    "chinese", "cumans", "ethiopians", "franks", "goths", "huns", "incas", "indians", "italians",
                    "japanese", "khmer", "koreans", "lithuanians", "magyars", "malay", "malians", "mayans", "mongols",
                    "persians", "portuguese", "saracens", "sicilians", "slavs", "spanish", "tatars", "teutons", "turks",
                    "vietnamese", "vikings"]

        if civ in all_civs:

            civ = civ.lower()

            chrome_options = Options()
            chrome_options.add_argument("--headless")

            path = "C:\chromedriver.exe"
            driver = webdriver.Chrome(path, options=chrome_options)

            driver.get("https://aoecompanion.com/civ-overviews/{}".format(civ))

            b = ""
            tb = ""
            un = ""
            te = ""

            # BONUSES
            bonuses = driver.find_elements_by_xpath(
                r'/html/body/div/div/div/div[1]/main/div/div/div[2]/div[2]/div/div/div[1]/div')

            for i in bonuses:
                b += i.text.replace("arrow_right\n", "").replace("Civilization Bonuses\n", "").replace("expand_more\n",
                                                                                                       "")
                # print(i.text.replace("arrow_right\n", "").replace("Civilization Bonuses\n", "").replace("expand_more\n", ""))

            # BONUSES TEAM
            team = driver.find_elements_by_xpath(
                '/html/body/div/div/div/div[1]/main/div/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div')

            for i in team:
                tb += i.text.replace("arrow_right\n", "")

            # BONUS UNIT
            unit = driver.find_elements_by_xpath(
                '/html/body/div/div/div/div[1]/main/div/div/div[2]/div[3]/div/section[1]/div')

            # print("\n--Unique Units--")
            for i in unit:
                un += i.text.replace("arrow_right\n", "").replace("info_outline\n", "").replace("Unique Units\n",
                                                                                                "").replace(
                    "Strengths and weaknesses\n", "").replace("expand_more", "")

            # BONUS TECH
            tech = driver.find_elements_by_xpath(
                '/html/body/div/div/div/div[1]/main/div/div/div[2]/div[3]/div/section[2]')
            for i in tech:
                te += i.text.replace("Unique Technologies\n", "")

            await ctx.channel.send(
                "**{}**\n\n**Civ bonuses**\n```{}```\n**Team bonuses**\n```{}```\n**Unique Units**\n```{}```\n**Unique Tech**\n```{}```".format(
                    civ.upper(), b, tb, un, te))

        else:
            await ctx.channel.send("Not a civ.")

    ###################################################################################

def setup(client):
    client.add_cog(aoe(client))
