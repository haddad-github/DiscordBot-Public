from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class foot(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def foot(self, ctx, parc):

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        # Locate chromedriver et utiliser chrome
        path = "C:\chromedriver.exe"
        driver = webdriver.Chrome(path, options=chrome_options)

        if parc == "###":
            driver.get("###")

        elif parc == "###":
            driver.get("###")

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

    ###################################################################################

def setup(client):
    client.add_cog(foot(client))
