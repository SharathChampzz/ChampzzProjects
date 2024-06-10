# load the token from the .env file
from dotenv import load_dotenv
import os
from .news_helper import NewsGeneratorHelper

load_dotenv()
TOKEN = os.getenv('TOKEN')

news_helper = NewsGeneratorHelper()

# Define the required directories
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
NEWS_IMAGES_DIRECTORY = os.path.join(CURRENT_DIRECTORY, os.getenv('NEWS_IMAGES_DIRECTORY_NAME'))
BIN_FOLDER = os.path.join(CURRENT_DIRECTORY, os.getenv('BIN_FOLDER_NAME'))
TO_BE_UPLOADED_FOLDER = os.path.join(CURRENT_DIRECTORY, os.getenv('TO_BE_UPLOADED_FOLDER_NAME'))

if not os.path.exists(BIN_FOLDER):
    os.mkdir(BIN_FOLDER)

if not os.path.exists(TO_BE_UPLOADED_FOLDER):
    os.mkdir(TO_BE_UPLOADED_FOLDER)
     
# import the required modules for discord
import discord
from discord.ext import commands

# Intents are required to access certain events like on_message
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True  # Enable reaction intents

bot = commands.Bot(command_prefix='!', intents=intents)

# Helper functions
def move_to_bin(image_name):
    try:
        print(f'Moving file to bin {image_name}')
        os.rename(os.path.join(NEWS_IMAGES_DIRECTORY, image_name), os.path.join(BIN_FOLDER, image_name))
    except Exception as e:
        print(f"Error moving file {image_name} to bin: {e}")

def move_to_upload_folder(image_name):
    try:
        print(f'Moving file to upload folder {image_name}')
        os.rename(os.path.join(NEWS_IMAGES_DIRECTORY, image_name), os.path.join(TO_BE_UPLOADED_FOLDER, image_name))
    except Exception as e:
        print(f"Error moving file {image_name} to upload folder: {e}")

async def upload_image(message: discord.Message, image_path:str):
  """Uploads an image to the channel."""
  if os.path.isfile(image_path):  # Check if image file exists
    with open(image_path, "rb") as f:
      image = discord.File(f)
      await message.channel.send(content="Image uploaded!", file=image)
  else:
    await message.channel.send("Error: Image file not found.")
    
@bot.event
async def on_ready() -> None:
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return
    
    if message.content.startswith("sendnews"):
        for image in os.listdir(NEWS_IMAGES_DIRECTORY):
            image_path = os.path.join(NEWS_IMAGES_DIRECTORY, image)
            print(f'Uploading : {image_path}')
            
            news_headline = str(image)
            sent_message = await message.channel.send(content=news_headline, file=discord.File(image_path))

    # Reply to a specific message
    elif message.content == 'hello':
        await message.channel.send('Hello! How can I help you today?')

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction: discord.Reaction, user):
    # Get message and reaction emoji
    message = reaction.message
    emoji = reaction.emoji
  
    print(f'Reaction Message: {message.content}')
    print(f'Reaction Emoji: {emoji}')
    

    if emoji == "👍":  # Check for thumbs up reaction
        move_to_upload_folder(message.content)
    else:
        move_to_bin(message.content)
        
    await reaction.message.channel.send(f'{user} reacted with {reaction.emoji}!')

@bot.command()
async def ping(ctx: commands.Context) -> None:
    await ctx.send('Pong!')

bot.run(TOKEN)

