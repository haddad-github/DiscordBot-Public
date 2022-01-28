import discord
from discord.ext import commands
from math import comb

class odds(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    ###################################################################################

    async def odds(self, ctx, nFoisGet=None, nAttempts=None, dropRate=None):

        if nFoisGet is None and nAttempts is None and dropRate is None:
            await ctx.channel.send("Format: *!odds [number of **times** you got the item] [number of **attempts**] [item **drop rate (1/x)**]*")

        else:

            dropRate = dropRate.split("/")
            dropRate = int(dropRate[0]) / float(dropRate[1])

            nFoisGet = int(nFoisGet)
            nAttempts = int(nAttempts)

            prob = comb(nAttempts, nFoisGet) * (dropRate**nFoisGet) * (1 - (dropRate))**(nAttempts - nFoisGet)

            chance = 1/prob

            pour = f"{round(prob*100,8)} %"
            sur_un = f"1/{round(chance)}"

            embed = discord.Embed(title=f'{pour} ..or.. {sur_un}')

        await ctx.channel.send(embed=embed)

    #####################################################################################

def setup(client):
    client.add_cog(odds(client))

