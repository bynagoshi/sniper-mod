import discord
from discord.ext import commands
import os

your_user_id = os.getenv["user_id"]
bot_token = os.getenv["bot_token"]

intents = discord.Intents.default()
intents.members = True  # This is necessary to track join events

bot = commands.Bot(command_prefix='!', intents=intents)

keyword = "sn1prz"


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')


@bot.event
async def on_member_join(member):
    if keyword.lower() in member.name.lower():
        user = bot.get_user(your_user_id)  # Get your user object
        if user:
            try:
                await user.send(f"A user with the keyword '{keyword}' in their name has joined: {member.name}")
            except discord.errors.Forbidden:
                print(
                    f"Could not send a message to {user.name}, they might have DMs disabled.")
            except Exception as e:
                print(f"An error occurred: {e}")

# Run the bot
# Replace with your bot's token
bot.run('{bot_token}')
