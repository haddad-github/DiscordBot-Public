import os
from google.cloud import translate_v2 as translate
from discord.ext import commands

class trans(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def translate(self, ctx, target, *,text):

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\rorop\Desktop\GoogleCoudKey.json"

        translate_client = translate.Client()

        output = translate_client.translate(text, target_language=target)

        await ctx.channel.send(output['translatedText'])


    ###################################################################################

def setup(client):
    client.add_cog(trans(client))