from discord.ext import commands
import lxml.html
from urllib.request import urlopen, Request
import re

class camel(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def camel(self, ctx, *, item):

        if " " in item:
            item = item.replace(" ", "+")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

        reg_url = "https://ca.camelcamelcamel.com/search?sq=" + item
        req = Request(url=reg_url, headers=headers)
        htmlx = urlopen(req).read()

        etree = lxml.html.fromstring(htmlx)
        code = etree.xpath('//*[@id="content"]/div[3]/div[1]/div[2]/div[1]/p/strong/a')

        name_list = []
        for i in code:
            name_list.append(i.text)

        name_full = name_list[0]
        code = name_full.split()[-1]
        code_final = code.replace("(", "").replace(")", "")

        reg_url2 = "https://ca.camelcamelcamel.com/product/" + code_final + "?context=search"
        req2 = Request(url=reg_url2, headers=headers)
        htmlx2 = urlopen(req2).read()

        #etree2 = lxml.html.fromstring(htmlx2)
        #graph = etree2.xpath('/html/body/div[4]/div[2]/div/div/div[5]/div/div[1]/div[1]/a/img/@src')

        str_htmlx2 = str(htmlx2)

        chart = re.findall("charts\.(.*)=en\";.*", str_htmlx2)

        chart_text = chart[0]

        await ctx.channel.send("https://charts." + chart_text + "=en")

    ###################################################################################

def setup(client):
    client.add_cog(camel(client))
