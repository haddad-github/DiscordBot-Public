import discord
from discord.ext import commands
import requests

class convert(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    ###################################################################################
    async def convert(self, ctx, num, fromm, to):

        fromm = fromm.upper()

        to = to.upper()

        if num[-1] == 'k':
            num = num[:-1]
            num = float(num)
            num = num * 1000

        elif num[-1] == 'm':
            num = num[:-1]
            num = float(num)
            num = num * 1000000

        elif num[-1] == 'b':
            num = num[:-1]
            num = float(num)
            num = num * 1000000000

        url = 'https://api.exchangerate.host/latest'
        response = requests.get(url)
        data = response.json()

        fromm_rate = float(data['rates'][fromm])
        to_rate = float(data['rates'][to])

        final = to_rate / fromm_rate * float(num)

        final = round(final,2)

        num = float(num)

        embed = discord.Embed(title=f'Converting {num:,} {fromm} to {to}')
        embed.add_field(name='Total', value=f'{final:,} $')
        embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmVkYRWtAiM_juhgCoc0h4PmixnakZ9ER4fA&usqp=CAU')

        await ctx.channel.send(embed=embed)

    ###################################################################################
def setup(client):
    client.add_cog(convert(client))