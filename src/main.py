import os 
import asyncio
import discord
from discord.ext import commands

from .bot.message_processing.process_message import process_message

from dotenv import load_dotenv
load_dotenv()

#---------------------------------------------Discord Code-------------------------------------------------
# Initialize Discord bot
defaultIntents = discord.Intents.default()
defaultIntents.message_content = True
bot = commands.Bot(command_prefix="!", intents=defaultIntents)

@bot.event
async def on_ready():
    try:
        print("----------------------------------------")
        print(f'✅ Bot has successfully logged  {bot.user}')
        print("✅ Commands have been synced with Discord")
        print("----------------------------------------")
    except Exception as e:
        print(f"❌ Command synchron: {e}")

@bot.event
async def on_message(message):
    asyncio.create_task(process_message(bot, message))
    
#---------------------------------------------Run Bot-------------------------------------------------
def run_bot():
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    if not discord_token:
        print("⚠️ DISCORD_TOKEN not found")
        return
    bot.run(discord_token)
