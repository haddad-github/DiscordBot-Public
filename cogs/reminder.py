import os
from discord.ext import commands
import pandas as pd
from datetime import datetime
from datetime import timedelta

class remindme(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()

    ###################################################################################

    async def remindme(self, ctx, integer, unit, *, message):
        '''Ex:
            !remindme [integer] [unit] [message]
            !remindme [15] [min] [take out the trash]'''

        # Get the user's ID
        userid = ctx.author.id

        # Turn integer into an int and get user's message
        integer = int(integer)
        message = message

        # Get date and time at the time the command was issued
        current_time = datetime.now()

        # Add the time requested to the current_time, to get the date and time of the reminder
        if unit == "sec":
            reminder_time = current_time + timedelta(seconds=integer)
        elif unit == "min":
            reminder_time = current_time + timedelta(minutes=integer)
        # elif unit == "hour":
        #     end = start + timedelta(hours=integer)
        # elif unit == "day":
        #     end = start + timedelta(days=integer)
        # elif unit == "week":
        #     end = start + timedelta(weeks=integer)
        # #Not natively supported; need to fix it
        # elif unit == "month":
        #     end = start + timedelta(weeks=integer*4)
        # elif unit == "year":
        #     end = start + timedelta(weeks=integer*52)

        # Read dataframe

        # Dataframe
        df = pd.read_csv("data.txt")

        # Append the user's id, current time, reminder time and the message to the dataframe
        df = df.append({"userid": userid, "start": current_time, "end": reminder_time, "message": message},
                       ignore_index=True)

        # Open the .txt file and rewrite the entire document with the newly appended row (reminder)
        with open("data.txt", "w") as f:
            df.to_csv(f, index=False)

        # Go through the dataframe...
        # Locate if any reminder_time has already passed (therefore smaller than the time right now)
        # Take the index of that row, the user's id and the message
        for i in range(len(df)):

            if str(df.iloc[i].reminder_time) <= str(datetime.now()):
                index = i  # row index
                id = df.iloc[i].userid  # user's id
                message = df.iloc[i].message  # user's message

                await ctx.author.send(
                    "Index {}:, userid:{}, message: {}".format(index, id, message))  # send reminder to user

                # Remove those row(s) from the dataframe because the user was reminded
                df.drop([index])
                with open("data.txt", "w") as f:
                    df.to_csv(f, index=False)

        # for time in df["end"]:
        #     if str(time) >= str(datetime.now()):
        #         #await ctx.author.send(df["message"])
        #         await ctx.channel.send(df["message"])

        # for time in df["end"]:
        #     if str(time) >= str(datetime.now()):
        #         #user = await Bot.fetch_user(userid)
        #         user = await client.fetch_user(userid)
        #         await user.send("test")

        # await ctx.channel.send(df)
        # await ctx.channel.send("Le request est passee a: {} et sera transmis a: {}".format(start, end))

    ###################################################################################

def setup(client):
    client.add_cog(remindme(client))
