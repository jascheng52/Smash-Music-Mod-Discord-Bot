import datetime
import sys
from xmlrpc.client import MAXINT
from time import sleep
import botExceptions as be
import nextcord as nc
from nextcord import Intents
from nextcord.ext import commands
import asyncio
import convertStartEnd
import Parameters
from audio import edit_audio
from downloadYou import download_urls
from Alerts import Alerts
intents = Intents.default()
intents.message_content = True
msg_limit = float("inf")

def bot_loop(token, channel_id,server_id,date, loop,botExcept):
    bot = commands.Bot(command_prefix="!", intents=intents, loop=loop)
    botExcept = botExcept
    @bot.command(name = "hi")
    async def sendMsg(interaction: nc.Interaction):
        if(interaction.channel.id == channel_id):
            await interaction.send("This is Testing")
        else:
            await interaction.send("This is Not Testing")
            await interaction.send("Current Channel_id: "+ interaction.channel.id)
            await interaction.send("Passed Channel_id: "+ channel_id)


    # @bot.command(name = "download")
    # @commands.is_owner()
    async def retrieveHistory(channel):
        date_start = datetime.datetime.combine(date, datetime.datetime.min.time())
        if(channel != None):
            try:
                print(channel)
                # arg = arg.split("/")
                # date_start = datetime.datetime(month = int(arg[0]),day = int(arg[1]), year = int(arg[2]))
                # await interaction.send("Downloading songs from " + 
                #     date_start.strftime("%m/%d/%Y"))
                print("Downloading songs from " + 
                    date_start.strftime("%m/%d/%Y"))
                download_counter = 0
                async for x in channel.history(after = date_start, limit = msg_limit):
                    msg = x.content
                    download_counter = download_counter + download_urls(msg)
                print(download_counter, "songs successfully download")
                
                # await interaction.send("Songs successfully downloaded")
                # await interaction.send("Compressing Songs ...")
                print("Compressing Downloaded Songs")
                edit_audio()
                # await interaction.send("Finished Song Compression")
                print("Finished Song Compression")
                # await interaction.send("Compressing Songs ...")
                # await interaction.send("Converting to smash audio ...")
                print("Converting to smash audio ...")
                count = convertStartEnd.convert_smash_audio()
                # await interaction.send("Finished conversion of " + str(count) + " songs!\nCheck the rename folder and error file/log for any errors")
                print(Alerts.DONE,"Finished conversion of " + str(count) + " songs!\nCheck the rename folder and error file/log for any errors")
                # await interaction.send(file = nc.File("squirtle.gif"))
                botExcept.done()
                await shutdown()
                return
            except ValueError:
                print("Please enter a valid date of mm/dd/yyyy")
                await shutdown()            
        else:
            return

    # @bot.command(name = "off")
    # @commands.is_owner()
    async def shutdown ():
        await bot.close()
        exit(1)


    @bot.event
    async def on_ready():      
        guild = bot.get_guild(server_id)
        try:
            if guild == None:
                raise be.InvalidServer
            channels = guild.channels
            for channel in channels:
                if channel.id == channel_id:
                    await retrieveHistory(channel)
                else:
                    if channel.type == nc.ChannelType.text:
                        threads = channel.threads
                        for thread in threads:
                            if thread.id == channel_id:
                                await retrieveHistory(thread)
            # channel = nc.utils.get(guild.channels, id=channel_id)

            # if channel == None:
            raise be.InvalidChannel
        except be.InvalidChannel as e:
            botExcept.set(e)
            await shutdown()
            return
        except be.InvalidServer as e:
            botExcept.set(e)
            await shutdown()
            return
        
        print("Sqirtle Bot is On")
        await retrieveHistory(channel)


    try:
        bot.run(token)
    except nc.errors.LoginFailure:
        raise be.InvalidToken

def Run_Bot(token,channel_id,date,server,botExcept):
    # print(token, channel_id,date,server)
    new_event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_event_loop)
    bot_loop(token=token,channel_id=channel_id,date=date,server_id=server, loop=new_event_loop,botExcept=botExcept)


# # print('failed run')
# try:
#     Run_Bot('')
# except Exception:
#     print('failed run')
# Run_Bot('MTAwNjMxMjA2NTI3Njg0MjE5NA.G1jtZx.macCJwbOm3je-BS-BBBz6Vx6uE8-a0SUSHdsuo')