from discord.ext import commands

# class remove(commands.Cog):
#
#     def __init__(self, client):
#         self.client = client
#
#     @commands.command()

    ###################################################################################

    # ctx = channel where it's being called
    # !remove [word]
    # removes all instances of that word
    # Counts number of messages deleted; starts count at n = -1 car command itself counts
    #@commands.haspermissions(administrator=True)
    #async def remove(self, ctx, word):
        #    n = -1
        #    async for message in ctx.channel.history(): #optional limit ; .history(limit=integer)
        #        if word in message.content.lower(): #recognizes word regardless of version (ex: bonjour = bOnJoUr)
        #            await message.delete()

        #        if message.content.find(word) != -1:
        #            n += 1

        #    await ctx.channel.send("J'ai delete {} instance(s) du mot".format(n)) #n = number of deleted messages

        #___________________________________________________________________________
        #Notes:
        #Works with spoiler words too

        #!remove [space] and !remove [ALT+255] does not remove messages; good
        ############################################################################

        ###################################################################################

# def setup(client):
#     client.add_cog(remove(client))