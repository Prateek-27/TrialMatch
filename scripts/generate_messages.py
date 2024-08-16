import pandas as pd
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Initialize the Groq client with your API key
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

# Function to generate personalized messages using Groq
def generate_personalized_message(content, author_name, sentiment, context="post"):
    prompt = f"Write a {sentiment} and informative message to a Reddit user named {author_name} who is interested in clinical trials. Their {context} was: \"{content}\". The message should encourage them to learn more about participating in clinical trials."

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )

    message = chat_completion.choices[0].message.content.strip()
    return message

# Load the sentiment-analyzed data
posts_df = pd.read_csv('data/reddit_posts_with_sentiment.csv')
comments_df = pd.read_csv('data/reddit_comments_with_sentiment.csv')

link = "https://forms.gle/sTM2a6LyNtmyjAw77"

def generate_personalized_message(content, author_name, sentiment, context="post"):
    if sentiment == "positive":
        prompt = f"Write a personalized message of maximum 100 words to the Reddit user named {author_name} who has shown high interest in clinical trials shown through a {context}. Here is the context that you can use to make it personalizable: {content}. End it with redirecting them to a google form: {link}. In the response you generate, Just generate the final message without any additional information before or after the message. Just the message without here it is or anything else, just the message"

    elif sentiment == "neutral":
        prompt = f"Write a personalized message of maximum 100 words to the Reddit user named {author_name} who has shown low interest in clinical trials shown through a {context}. Here is the context that you can use to make it personalizable: {content}. End it with redirecting them to a google form: {link}. In the response you generate, Just generate the final message without any additional information before or after the message. Just the message without here it is or anything else, just the message"

    else:
        prompt = f"Write a personalized message of maximum 100 words to the Reddit user named {author_name} who has shown concern in clinical trials shown through a {context}. Here is the context that you can use to make it personalizable: {content}. End it with redirecting them to a google form: {link}. In the response you generate, Just generate the final message without any additional information before or after the message. Just the message without here it is or anything else, just the message"


    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )

    message = response.choices[0].message.content.strip()
    return message


# Generate messages for posts
post_messages = []
for index, row in posts_df.iterrows():
    author_name = row['author']
    post_content = row['body']
    sentiment = row['sentiment_category']  # Use the pre-segmented interest level
    message = generate_personalized_message(post_content, author_name, sentiment, context="post")
    post_messages.append([author_name, post_content, sentiment, message])

# Generate messages for comments with combined post and comment content
comment_messages = []
for index, row in comments_df.iterrows():
    author_name = row['author']
    comment_content = row['body']
    post_id = row['post_id']  # Assuming you have a post_id column linking comments to posts
    post_content = posts_df.loc[posts_df['id'] == post_id, 'body'].values[0]  # Get the original post content
    combined_content = f"Post: {post_content}\nComment: {comment_content}"  # Combine post and comment content
    sentiment = row['sentiment_category']  # Use the pre-segmented interest level
    message = generate_personalized_message(combined_content, author_name, sentiment, context="comment")
    comment_messages.append([author_name, combined_content, sentiment, message])

# Save the messages to a CSV file
def save_messages_to_csv(messages, filename='data/personalized_messages.csv'):
    messages_df = pd.DataFrame(messages, columns=['author', 'content', 'interest_level', 'personalized_message'])
    messages_df.to_csv(filename, index=False)
    print(f"Messages saved to {filename}")

# Combine post and comment messages
all_messages = post_messages + comment_messages

# Save the messages to a CSV
save_messages_to_csv(all_messages)