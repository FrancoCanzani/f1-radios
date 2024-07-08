import os
import tweepy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

client = tweepy.Client(
    consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
)

def post_tweet(text: str):

    try:
        client.create_tweet(text=text)            
        print("Tweet posted successfully.")
        
    except tweepy.TweepError as e:
        print(f"Error: {e}")
