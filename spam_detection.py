import discord
from collections import defaultdict
from datetime import datetime, timedelta
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

    async def handle_spam(self, message_content):
        for message in self.messages[message_content]:
            try:
                await message.delete()
            except discord.errors.NotFound:
                # Message already deleted
                pass
            except discord.errors.Forbidden:
                print("Bot does not have permissions to delete messages.")
