# load the token from the .env file
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

# import the required modules for discord
import discord
from discord.ext import commands

# Intents are required to access certain events like on_message
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready() -> None:
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.event
async def on_message(message: discord.Message) -> None:
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Reply to a specific message
    if message.content == 'hello':
        await message.channel.send('Hello! How can I help you today?')

    await bot.process_commands(message)

@bot.command()
async def ping(ctx: commands.Context) -> None:
    await ctx.send('Pong!')

bot.run(TOKEN)