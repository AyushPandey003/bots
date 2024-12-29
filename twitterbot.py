import discord
from discord.ext import commands, tasks
import tweepy
from dotenv import load_dotenv
import os
load_dotenv()

# Discord Bot Token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Twitter API Keys
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
YOUR_DISCORD_CHANNEL_ID = os.getenv("YOUR_DISCORD_CHANNEL_ID")

# Initialize Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)

# Initialize Discord Bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# List of Twitter accounts to track (by username)
TRACKED_ACCOUNTS = ["elonmusk", "nasa", "spacex"]

# Keep track of last seen tweet IDs
last_seen_tweet = {}

async def fetch_tweets_v2(username):
    tweets = twitter_api.user_timeline(screen_name=username, count=6, tweet_mode="extended")
    return tweets

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    check_tweets.start()  # Start the tweet-checking loop
@bot.command()
async def ping(ctx):
    await ctx.send("Bot is working!")

@tasks.loop(seconds=3600)  # Check every 10 seconds
async def check_tweets():
   async def check_tweets():
    channel = bot.get_channel(YOUR_DISCORD_CHANNEL_ID)  # Replace with your channel ID
    for username in TRACKED_ACCOUNTS:
        tweets = await fetch_tweets_v2(username)
        for tweet in tweets:
            tweet_url = f"https://twitter.com/{username}/status/{tweet.id}"
            await channel.send(f"New tweet from @{username}: {tweet.text}\n{tweet_url}")
# Run the bot
bot.run(DISCORD_TOKEN)
