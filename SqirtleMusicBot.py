import datetime
import sys
from xmlrpc.client import MAXINT

import nextcord as nc
from nextcord import Intents
from nextcord.ext import commands

import convertStartEnd
import Parameters
from audio import edit_audio
from downloadYou import download_urls

intents = Intents.default()
intents.message_content = True
msg_limit = float("inf")

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(name = "hi")
async def sendMsg(interaction: nc.Interaction):
    if(interaction.channel.id == Parameters.GUILD_ID):
        await interaction.send("This is Testing")
    
    else:
        await interaction.send("This is Not Testing")


@bot.command(name = "download")
@commands.is_owner()
async def retrieveHistory(interaction: nc.Interaction, arg):
    if(interaction.channel.id == Parameters.GUILD_ID):
        try:
            arg = arg.split("/")
            date_start = datetime.datetime(month = int(arg[0]),day = int(arg[1]), year = int(arg[2]))
            await interaction.send("Downloading songs from " + 
                date_start.strftime("%m/%d/%Y"))
            async for x in interaction.channel.history(after = date_start, limit = msg_limit):
                msg = x.content
                download_urls(msg)
            print("Songs successfully download successfully created")
            await interaction.send("Songs successfully downloaded")
            await interaction.send("Compressing Songs ...")
            edit_audio()
            await interaction.send("Finished Song Compression")
            await interaction.send("Converting to smash audio ...")
            count = convertStartEnd.convert_smash_audio()
            await interaction.send("Finished conversion of " + str(count) + " songs!\nCheck the rename folder and error file/log for any errors")
            await interaction.send(file = nc.File("squirtle.gif"))
        except ValueError:
            await interaction.send("Please enter a valid date of mm/dd/yyyy")
        
    else:
        return


@bot.command(name = "off")
@commands.is_owner()
async def shutdown(interaction: nc.Interaction):
    await bot.close()

@bot.event
async def on_ready():
    print("Hello this is sqirtle")



bot.run(Parameters.BOT_TOKEN)
