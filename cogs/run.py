import subprocess
from discord.ext import commands
import discord

class run(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def run(self, ctx, *, string):
        string = string.strip("```").replace("python\n", "")

        print(string)

        exec(f"{string}")

        res = subprocess.check_output(["python", "-c", string])

        resFinal = res.decode('utf-8')

        embed = discord.Embed(title="Ton code donne ca:")
        embed.add_field(name="________", value=resFinal)

        await ctx.channel.send(embed=embed)


    ###################################################################################

def setup(client):
    client.add_cog(run(client))