import discord
from discord.ext import commands
import os
from username_detection import check_username
from spam_detection import SpamDetector

your_user_id = int(os.getenv("user_id"))
bot_token = os.getenv("bot_token")

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize SpamDetector
spam_detector = SpamDetector()

# List of keywords to check
keywords = ["anotherkeyword", "example"]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')


# @bot.event
# async def on_member_join(member):
#     # Call the function from the other file
#     await check_username(member, bot, keywords, your_user_id)


@bot.event
async def on_message(message):
    # Avoid processing messages sent by the bot
    if message.author == bot.user:
        return

    # Check for spam messages
    await spam_detector.check_message(message)

    # Process commands
    await bot.process_commands(message)

bot.run(bot_token)
