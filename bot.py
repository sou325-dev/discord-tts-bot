import os
import asyncio
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import requests


TOKEN = "TOKEN"
VOICEVOX_HOST = "127.0.0.1"  
VOICEVOX_PORT = 50021       
SPEAKER_ID = 3               

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

vc_dict = {}  

os.makedirs("./temp", exist_ok=True)

def create_voice(text: str, path: str):
    query = requests.post(
        f"http://{VOICEVOX_HOST}:{VOICEVOX_PORT}/audio_query",
        params={"text": text, "speaker": SPEAKER_ID}
    ).json()

    wav = requests.post(
        f"http://{VOICEVOX_HOST}:{VOICEVOX_PORT}/synthesis",
        params={"speaker": SPEAKER_ID},
        json=query
    ).content

    with open(path, "wb") as f:
        f.write(wav)

@bot.command()
async def join(ctx):
    """BotをVCに参加させる"""
    if ctx.author.voice:
        guild_id = ctx.guild.id
        if guild_id in vc_dict and vc_dict[guild_id].is_connected():
            await ctx.send("すでにVCに接続しています")
            return
        vc = await ctx.author.voice.channel.connect()
        vc_dict[guild_id] = vc
        await ctx.send(f"VCに参加しました: {ctx.author.voice.channel.name}")
    else:
        await ctx.send("先にVCに入ってね！")

@bot.command()
async def leave(ctx):
    """BotをVCから退出させる"""
    guild_id = ctx.guild.id
    if guild_id in vc_dict:
        vc = vc_dict[guild_id]
        if vc.is_playing():
            vc.stop()
        await vc.disconnect()
        vc_dict.pop(guild_id)
        await ctx.send("VCから退出しました")



@bot.event
async def on_message(message):
    
    if message.author.bot:
        return

    await bot.process_commands(message)  

    guild_id = message.guild.id
    if guild_id not in vc_dict:
        return  

    vc = vc_dict[guild_id]
    if not vc.is_connected():
        return

    text = message.content
    filename = f"./temp/{guild_id}.wav"
    create_voice(text, filename)

    
    if vc.is_playing():
        vc.stop()
    vc.play(FFmpegPCMAudio(filename))

    
    while vc.is_playing():
        await asyncio.sleep(0.5)

    os.remove(filename)


bot.run(TOKEN)
