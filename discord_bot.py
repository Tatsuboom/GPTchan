import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import gpt_api
import voicevox_api

# .envからディスコードのトークンを読み込む
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True
client = commands.Bot(command_prefix='!',intents=intents)

voiceclient = None

#起動処理
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user or len(message.mentions) >= 2 :
        await client.process_commands(message)
        return
    if client.user in message.mentions and not message.mention_everyone:
        content = message.content.replace('<@1373748611866820739>','')
        if content == None or len(content) <= 1:
            await message.reply("呼んだ？")
            await client.process_commands(message)
            return
        
        async with message.channel.typing():
            output_text = gpt_api.createTextResponse(content)
            if output_text:
                if voiceclient != None and voiceclient.is_connected():
                    voicevox_api.createvoice(output_text)
                    voiceclient.play(discord.FFmpegPCMAudio("output.wav"))

                await message.reply(output_text)
    await client.process_commands(message)

#応答生成(コマンド版)
@client.command()
async def talk(ctx,*, message: str = None):
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

#ボイスチャンネルに誰もいなくなったら自動退出
@client.event
async def on_voice_state_update(member,before,after):
    global voiceclient
    if voiceclient == None: return
    if len(voiceclient.channel.members) <= 1:
        await voiceclient.disconnect()
        voiceclient = None

client.run(DISCORD_TOKEN)

