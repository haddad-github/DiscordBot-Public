import os
from discord.ext import commands

#"!" becomes the prefix for all commands (ex: !ping)
client = commands.Bot(command_prefix = "!")

#Indicates if bot is active
@client.event #event ([variable].event)
async def on_ready():
    print("Bot is ready.")

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

#Looking through all files in cogs directory (specifically .py files)
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')#removes .py

##################################################################

#All commands
@client.command()
async def commands(ctx):

    await ctx.channel.send("```"
                           "\n!anime [anime name] : gives anime info (rating/eps/etc.)\n"
                           "\n!aoe [civilization] : gives civ's uniques\n"
                           "\n!camel [item] : gives graph of item's price through time, including highest and lowest\n"
                           "\n!coin [crypto coin/token] : gives price and daily change of the coin/token\n"
                           "\n!covid : gives Covid stats today\n"
                           "\n!et [word] : gives word etymology\n"
                           "\n!flip : pile ou face\n"
                           "\n!gas [~~/~~] : gives gas price\n"
                           "\n!ge [item] : gives OSRS item price and change overtime\n"
                           "\n!table [england/spain/italy/germany] : gives football/soccer league table\n"
                           "\n!weather : gives 8 days forecast\n"
                           "\n!foot [~~/~~] : gives park availability\n"
                           "\n[OFFLINE] !remindme [unit] [time unit] [message] : reminder (ex:!remind me 5 min take out the trash\n"
                           "\n!steam [game] : gives Steam game and discount (if available)\n"
                           "\n!stock [NASDAQ] : gives Stock's relevant information (current price, change, volume, etc.)"
                           "```")

##################################################################

#Must be the last line of code
client.run("TOKEN HERE")