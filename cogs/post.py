import os
import discord
from discord.ext import commands
import random

class post(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def post(self, ctx, link):
        # Execute download.exe + link
        os.chdir(r"C:\Users\rorop\Desktop\youtube-dl")

        os.system('youtube-dl -f best ' + link)

        a = os.listdir(r"C:\Users\rorop\Desktop\youtube-dl")
        latest = max(a, key=os.path.getctime)

        if latest[-3:] == 'mp4':
            await ctx.channel.send(file=discord.File(r"C:\Users\rorop\Desktop\youtube-dl\\" + latest))
            os.remove(r"C:\Users\rorop\Desktop\youtube-dl\\" + latest)
        else:
            await ctx.channel.send('Pas de mp4')

    ###################################################################################

def setup(client):
    client.add_cog(post(client))
