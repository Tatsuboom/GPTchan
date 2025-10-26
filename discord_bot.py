import os
import discord
import logging
import asyncio
import time
from discord.ext import commands
from dotenv import load_dotenv
import gpt_api
import voicevox_api

#トークンの読み込み、初期状態の設定
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True
client = commands.Bot(command_prefix='!',intents=intents)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


voiceclient = None

#起動処理
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

#会話生成
async def conversation(text):
    if text.content == None or len(text.content) <= 1:
        await text.channel.send("よんだ？")
        return
        
    async with text.channel.typing():
        start_gpt = time.perf_counter() #Timetest
        output_text = await asyncio.to_thread(gpt_api.createTextResponse,text.content)
        end_gpt = time.perf_counter() #Timetest
        if output_text:
            if voiceclient != None and voiceclient.is_connected():
                start_voice = time.perf_counter() #Timetest
                await asyncio.to_thread(voicevox_api.createvoice,output_text)
                voiceclient.play(discord.FFmpegPCMAudio("output.wav"))
                end_voice = time.perf_counter() #Timetest
            await text.channel.send(output_text)
            print(f"GPT生成時間: {end_gpt - start_gpt:.2f} 秒") #Timetest
            print(f"音声生成時間: {end_voice - start_voice:.2f} 秒") #Timetest

#メンションでの会話
@client.event
async def on_message(message):
    if client.user in message.mentions and not message.mention_everyone:
        message.content = message.content.replace('<@1373748611866820739>','')
        await conversation(message)

    await client.process_commands(message)

#コマンドでの会話
@client.command()
async def talk(ctx):
    ctx.message.content = ctx.message.content.replace('!talk','')
    await conversation(ctx.message)

#ロール追加
@client.command()
async def roll(ctx):
    roll = ctx.message.content.replace('!roll','')
    roll = roll.replace('\n','').strip()

    if len(roll) > 30:
        await ctx.channel.send("ながすぎておぼえられないよ！")
        return
    
    if not roll:
        await ctx.channel.send("なにをおぼえてほしいの？")
        return

    file_path = 'SubRolls.txt'
    try:
        if os.path.exists(file_path):
            with open('SubRolls.txt', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                items = [s for s in content.split('\n') if s.strip()]
        else:
            items = []

        items.insert(0, roll)
        items = items[:10]

        with open(file_path,'w',encoding='utf-8') as f:
            f.write('\n'.join(items))    
    except Exception as e:
        await ctx.channel.send(f"えらーえらーえらー！: {e}")
        return

    await ctx.channel.send(roll + "！おぼえた！")

#ボイスチャンネル接続
@client.command()
async def vc(ctx):
    global voiceclient
    if ctx.author.voice == None:
        await ctx.channel.send("ボイスチャンネルにいないじゃん！")
        return
    
    voiceclient = await ctx.author.voice.channel.connect()
    await ctx.channel.send("きたよー")
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

client.run(DISCORD_TOKEN,log_handler=handler)