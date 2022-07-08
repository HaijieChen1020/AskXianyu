# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from helper.logger import logger
from helper.roll_helper import roll_dice
from helper.reset_helper import get_reset_remains
from helper.boss_helper import get_boss_data
from helper.youtube_helper import YTDLSource
from exception.exceptions import InvalidNumberException

# load discord application token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_NAME')
DEVELOPER_EMAIL = os.getenv('DEV_EMAIL')

intents = discord.Intents().all()
client = discord.Client(intents=intents)
# set prefix to '!'
client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    logger.info(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, 欢迎来到{GUILD}!<3'
    )

@client.command(name='reset', help='return remaining time until next reset')
async def on_command(ctx):
    await ctx.send(get_reset_remains())

@client.command(name='boss', help='check boss stats, arg1 stands for boss name, has to be exactly same as in the game')
async def on_command(ctx, arg1):
    if not arg1:
        await ctx.send('missing boss name, please re-enter!')
    output = get_boss_data(arg1)
    print(type(output))
    if output.empty:
        await ctx.send('no info for boss {arg1}!')
    # Use embed here to better format the output table
    embed = discord.Embed(title="BOSS info: LUCID", description='```' + output.to_markdown() + '```') 
    await ctx.send(embed=embed)
    
@client.command(name='roll', help='roll random number between 1-100 by default, you can change the lower and upper bound by providing args [lower, upper]')
async def roll(ctx, arg1="1", arg2="100"):
    try:
        # roll点功能 with range
        roll_output = roll_dice(arg1, arg2)
        await ctx.send(roll_output)
    except InvalidNumberException as ex:
        await ctx.send(f"Invalid args: {str(ex)}")
    except Exception as ex:
        logger.error(str(ex))
        await ctx.send(f"Unknown error please reach out to {DEVELOPER_EMAIL}")


@client.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

# youtube manipulate part
@client.command(name='play', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=client.loop)
            voice_channel.play(discord.FFmpegPCMAudio(source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except Exception as ex:
        logger.error(str(ex))
        await ctx.send("Can't play the url you provided.")


@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@client.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@client.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


client.run(TOKEN)
