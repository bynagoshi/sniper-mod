import discord
from collections import defaultdict
from datetime import datetime, timedelta
from discord.ext import commands
import pytz


class SpamDetector:
    def __init__(self, time_frame=timedelta(seconds=10)):
        # Dictionary to store messages and their timestamps
        self.messages = defaultdict(list)
        self.time_frame = time_frame

    async def check_message(self, message):
        # Clean up old messages
        self.cleanup()

        # Add new message to tracking
        self.messages[(message.channel.id, message.content)].append(message)

        # Check for spam (same message in the same or multiple channels)
        if len(self.messages[(message.channel.id, message.content)]) > 1:
            await self.handle_spam(message.content, message.channel.id)

    def cleanup(self):
        utc = pytz.UTC
        current_time = datetime.now(utc)

        for content in list(self.messages.keys()):
            self.messages[content] = [msg for msg in self.messages[content]
                                      if current_time - msg.created_at < self.time_frame]
            if not self.messages[content]:
                del self.messages[content]

    async def handle_spam(self, message_content, channel_id):
        spamming_users = set()
        for message in self.messages[(channel_id, message_content)]:
            spamming_users.add(message.author)

            # Delete messages
            try:
                await message.delete()
            except discord.errors.NotFound:
                pass  # Message already deleted
            except discord.errors.Forbidden:
                print("Bot does not have permissions to delete messages.")

        # Apply timeout to users
        for user in spamming_users:
            try:
                # Timeout for 1 day
                await user.timeout(timedelta(minutes=1440))
                # await user.send(f"You have been timed out for 1 day due to spamming.")
            except discord.errors.Forbidden:
                print(f"Bot does not have permissions to timeout {user.name}.")
