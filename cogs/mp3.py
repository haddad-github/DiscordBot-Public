import os
import discord
from discord.ext import commands

class mp3(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def mp3(self, ctx, link):
        os.chdir(r"C:\Users\rorop\Desktop\youtube-dl")

        os.system('youtube-dl --extract-audio --audio-format mp3 ' + link)

        a = os.listdir(r"C:\Users\rorop\Desktop\youtube-dl")
        latest = max(a, key=os.path.getctime)

        if latest[-3:] == 'mp3':
            await ctx.channel.send(file=discord.File(r"C:\Users\rorop\Desktop\youtube-dl\\" + latest))
            os.remove(r"C:\Users\rorop\Desktop\youtube-dl\\" + latest)
        else:
            await ctx.channel.send('Pas un mp3')

    ###################################################################################

def setup(client):
    client.add_cog(mp3(client))
