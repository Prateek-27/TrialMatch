import praw
import pandas as pd
import os
from dotenv import load_dotenv
from praw.exceptions import RedditAPIException

# Load environment variables
load_dotenv()

# Initialize the Reddit client with your credentials
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"), 
    password=os.getenv("REDDIT_PASSWORD") 
)

messages_df = pd.read_csv('data/personalized_messages.csv')

def send_message(username, message_content):
    try:
        reddit.redditor(username).message(subject='Regarding Clinical Trials', message=message_content)
        print(f"Message sent to {username}")
    except RedditAPIException as e:
        print(f"Reddit API error occurred while messaging {username}: {e}")
    except Exception as e:
        print(f"Failed to send message to {username}: {e}")

for index, row in messages_df.iterrows():
    username = row['author']
    message_content = row['personalized_message']
    send_message(username, message_content)
