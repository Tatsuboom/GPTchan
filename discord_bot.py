import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import gpt_api
import voicevox_api

# .env から ディスコードのトークンを読み込む
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True
client = commands.Bot(command_prefix='!',intents=intents)

voiceclient = None

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

 #応答生成
@client.command()
async def gpt(ctx,*, message: str = None):
    if message == None or len(message) <= 1:
        await ctx.channel.send("呼んだ？")
        return
        
    async with ctx.typing():
        output_text = gpt_api.createTextResponse(message)
        if output_text:
            if voiceclient != None and voiceclient.is_connected():
                voicevox_api.createvoice(output_text)
                voiceclient.play(discord.FFmpegPCMAudio("output.wav"))

            await ctx.channel.send(output_text)
            


#ボイスチャンネル接続
@client.command()
async def vc(ctx):
    global voiceclient
    if ctx.author.voice == None:
        await ctx.channel.send("ボイスチャンネルにいないじゃん！")
        return
    
    voiceclient = await ctx.author.voice.channel.connect()
    await ctx.channel.send("来たよー")
    return

#ボイスチャンネル退出
@client.command()
async def leave(ctx):
    global voiceclient
    if voiceclient == None:
        await ctx.channel.send("ボイスチャンネルにはいないよー")
        return
    
    await voiceclient.disconnect()
    await ctx.channel.send("ばいばーい")
    voiceclient = None
    return

#ボイスチャンネルが誰もいなくなったら自動退出
@client.event
async def on_voice_state_update(member,before,after):
    global voiceclient
    if voiceclient == None:
        return
    members = voiceclient.channel.members
    if len(members) <= 1:
        await voiceclient.disconnect()
        voiceclient = None

client.run(DISCORD_TOKEN)

