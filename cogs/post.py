import os
import discord
from discord.ext import commands
import random

class post(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def post(self, ctx, link, fromm = None, to = None):
        # Execute download.exe + link
        os.chdir(r"C:\Users\###\Desktop\youtube-dl")

        if fromm == None and to == None:
            os.system("youtube-dl -f best "+ link + " -o %(title).20s.%(ext)s")
            #subprocess.run(["youtube-dl", "-f", "best", link, "-o", '%(title).20s.%(ext)s'])

        elif fromm is not None and to is not None:

            os.system(f'youtube-dl --postprocessor-args "-ss {fromm} -to {to}" {link} -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]"')

        a = os.listdir(r"C:\Users\###\Desktop\youtube-dl")
        latest = max(a, key=os.path.getctime)

        if latest[-3:] == 'mp4':
            await ctx.channel.send(file=discord.File(r"C:\Users\###\Desktop\youtube-dl\\" + latest))
            os.remove(r"C:\Users\###\Desktop\youtube-dl\\" + latest)
        else:
            await ctx.channel.send('Pas de mp4')

    ###################################################################################

def setup(client):
    client.add_cog(post(client))
