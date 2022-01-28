import discord
from discord.ext import commands
import youtube_dl
import nacl
import ffmpeg

class music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def play(self, ctx, *url):
        #If no author, send warning
        if ctx.author.voice is None:
            await ctx.send("T'es pas dans un channel")

        #Store the voice channel
        voice_channel = ctx.author.voice.channel

        #If bot is not in a voice channel, wait until connected
        #else move to the correct voice channel (switching channels)
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {"format":"bestaudio"}
        vc = ctx.voice_client

        if ".com" in url:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, executable=r"C:###\youtube-dl\ffmpeg.exe")
                await ctx.channel.send("Playing ton beat de merde")
                vc.play(source)

        else:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)
                print(info)
                print(info['entries'][0])
                urlx = info['entries'][0]
                url2 = urlx['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2,executable=r"C:###\youtube-dl\ffmpeg.exe")
                await ctx.channel.send(f"Playing: {urlx['title']}")
                vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("J'ai pause ton beat")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("J'ai resume ton beat")

###################################################################################

def setup(client):
    client.add_cog(music(client))

