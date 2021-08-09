from discord.ext import commands
import random

class flip(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def flip(self, ctx):
        choix = ("Pile", "Face")
        coin = random.choice(choix)

        await ctx.channel.send(coin)

    ###################################################################################

def setup(client):
    client.add_cog(flip(client))
