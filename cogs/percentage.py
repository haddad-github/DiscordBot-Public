import discord
from discord.ext import commands


class percentage(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    ###################################################################################

    async def diff(self, ctx, inn, out):

        inn = float(inn)
        out = float(out)

        perc = round((out / inn) - 1, 3) * 100

        if perc > 0:

            perc = f'+{perc}%'

        elif perc < 0:

            perc = f'{perc}%'

        # embed = discord.Embed(title=f'From {inn} to {out}')
        embed = discord.Embed(title='')
        embed.add_field(name='From:', value=inn)
        embed.add_field(name='To: ', value=out)
        embed.add_field(name="Change: ", value=perc)

        await ctx.channel.send(embed=embed)

    ###################################################################################


def setup(client):
    client.add_cog(percentage(client))
