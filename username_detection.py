import discord

# This function checks for the specific username


async def check_username(member, bot, keywords, your_user_id):
    for keyword in keywords:
        if keyword.lower() in member.name.lower():
            await notify_user(bot, your_user_id, member, keyword)
            break  # Break after the first match to avoid multiple notifications for the same member

# This function handles the notification


async def notify_user(bot, your_user_id, member, keyword):
    user = bot.get_user(your_user_id)  # Get your user object
    if user:
        try:
            await user.send(f"A user with the keyword '{keyword}' in their name has joined: {member.name}")
        except discord.errors.Forbidden:
            print(
                f"Could not send a message to {user.name}, they might have DMs disabled.")
        except Exception as e:
            print(f"An error occurred: {e}")
