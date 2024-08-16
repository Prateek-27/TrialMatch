import os
import praw, prawcore
import pandas as pd
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Reddit API credentials
reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
reddit_user_agent = os.getenv("REDDIT_USER_AGENT")

reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent
)

# Function to read subreddits for text file
def get_subreddits_from_file(filename='subreddits.txt'):
    with open(filename, 'r') as file:
        subreddits = [line.strip() for line in file.readlines()]
    return subreddits

# Function to read keywords for text file
def get_keywords_from_file(filename='keywords.txt'):
    with open(filename, 'r') as file:
        subreddits = [line.strip() for line in file.readlines()]
    return subreddits

subreddits = get_subreddits_from_file('subreddits.txt')
keywords = get_keywords_from_file('keywords.txt')

#print(keywords, subreddits)

# Function to scrape posts
def scrape_posts(subreddits, keywords, limit=100):
    posts_data = []
    for subreddit in subreddits:
        try:
            subreddit_instance = reddit.subreddit(subreddit)
            for submission in subreddit_instance.new(limit=limit):
                title = submission.title
                if any(keyword in title.lower() for keyword in keywords):
                    post = {
                        'id': submission.id,
                        'title': submission.title,
                        'body': submission.selftext,
                        'score': submission.score,
                        'comments': submission.num_comments,
                        'created_utc': submission.created_utc,
                        'subreddit': subreddit,
                        'author': submission.author.name if submission.author else 'N/A'
                    }
                    posts_data.append(post)
        except prawcore.exceptions.Redirect:
            print(f"Subreddit '{subreddit}' does not exist or is inaccessible. Skipping...")
        except Exception as e:
            print(f"An error occurred with subreddit '{subreddit}': {e}")
    return posts_data


# Function to scrape comments
def scrape_comments(post_ids, limit=100):
    comments_data = []
    for post_id in post_ids:
        submission = reddit.submission(id=post_id)
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            comment_data = {
                'post_id': post_id,
                'comment_id': comment.id,
                'body': comment.body,
                'score': comment.score,
                'created_utc': comment.created_utc,
                'author': comment.author.name if comment.author else 'N/A' 
            }
            comments_data.append(comment_data)
    return comments_data

# Function to save scaped data into a csv file
def save_to_csv(data, filename):
    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(data)
    # Save the DataFrame to a CSV file
    df.to_csv(f'data/{filename}.csv', index=False)
    print(f"Data saved to data/{filename}.csv")

posts_data = scrape_posts(subreddits, keywords, limit=1000)

save_to_csv(posts_data, 'reddit_posts')

post_ids = [post['id'] for post in posts_data]

comments_data = scrape_comments(post_ids, limit=200)

save_to_csv(comments_data, 'reddit_comments')