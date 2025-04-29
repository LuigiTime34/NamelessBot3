import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

HENRY_TOKEN = os.getenv("DISCORD_TOKEN_HENRY")
BEAR_TOKEN = os.getenv("DISCORD_TOKEN_BEAR")

if not HENRY_TOKEN:
    print("Error: DISCORD_TOKEN_HENRY not found in .env file!")
    exit(1)
if not BEAR_TOKEN:
    print("Error: DISCORD_TOKEN_BEAR not found in .env file!")
    exit(1)

# Use the same intents for both for simplicity, adjust if needed
intents = discord.Intents.default() # Start with defaults (includes guilds, messages, reactions, etc.)
intents.message_content = True    # Explicitly add the Message Content intent

# --- Create Separate Bot Instances ---
# Each bot needs its own instance to connect with its own token
bot_henry = commands.Bot(command_prefix="!", intents=intents)
bot_bear = commands.Bot(command_prefix="!", intents=intents)

# --- Henry's Event Handlers ---
# Use the specific bot instance decorator (@bot_henry.event)
@bot_henry.event
async def on_ready():
    print(f"--- {bot_henry.user} (Henry) is online! ---")

@bot_henry.event
async def on_message(message):
    # Don't respond to messages from the bot itself (Henry)
    if message.author == bot_henry.user:
        return
    # Don't respond to messages from the *other* bot (Bear) either
    if message.author == bot_bear.user:
        return

    # Check if Henry was mentioned
    # Use bot_henry.user here
    if bot_henry.user.mentioned_in(message):
        print(f"Henry mentioned by {message.author} in {message.channel}") # Log mention
        await message.channel.send("I just [REDACTED] your mom!")

    # If Henry ever gets commands, process them here:
    # await bot_henry.process_commands(message)


# --- Bear's Event Handlers ---
# Use the specific bot instance decorator (@bot_bear.event)
@bot_bear.event
async def on_ready():
    print(f"--- {bot_bear.user} (Bear) is online! ---")

@bot_bear.event
async def on_message(message):
    # Don't respond to messages from the bot itself (Bear)
    if message.author == bot_bear.user:
        return
    # Don't respond to messages from the *other* bot (Henry) either
    if message.author == bot_henry.user:
        return

    # Check if Bear was mentioned
    # Use bot_bear.user here
    if bot_bear.user.mentioned_in(message):
        print(f"Bear mentioned by {message.author} in {message.channel}") # Log mention
        await message.channel.send("THERE'S AN ECLIPSEEE")

    # If Bear ever gets commands, process them here:
    # await bot_bear.process_commands(message)


# --- Main Async Function to Start Both Bots ---
async def main():
    # Use asyncio.gather to run both bot startup routines concurrently
    # bot.run() blocks, but bot.start() is async and doesn't block the main thread
    print("Attempting to start both bots...")
    await asyncio.gather(
        bot_henry.start(HENRY_TOKEN),
        bot_bear.start(BEAR_TOKEN)
    )

# --- Run the Main Function ---
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Shutting down...")
        # Note: Proper graceful shutdown (closing connections) with asyncio.gather
        # and KeyboardInterrupt requires more complex signal handling within the
        # async main function. For these simple bots, Ctrl+C killing the
        # process is usually sufficient.
    finally:
        print("Combined bot script finished.")