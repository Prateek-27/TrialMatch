import pandas as pd
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# Load the sentiment-analyzed data
posts_df = pd.read_csv('data/reddit_posts_with_sentiment.csv')
comments_df = pd.read_csv('data/reddit_comments_with_sentiment.csv')

link = "https://forms.gle/sTM2a6LyNtmyjAw77"

# Function to generate personalized messages using OpenAI
def generate_personalized_message(content, author_name, sentiment, context="post"):
    if sentiment == "positive":
        prompt = f"Write a personalized message of maximum 100 words to the Reddit user named {author_name} who has shown high interest in clinical trials shown through a {context}. Here is the context that you can use to make it personalizable: {content}. End it with redirecting them to a google form: {link}. In the response you generate, Just generate the final message without any additional information before or after the message. Just the message without here it is or anything else, just the message"

    elif sentiment == "neutral":
        prompt = f"Write a personalized message of maximum 100 words to the Reddit user named {author_name} who has shown low interest in clinical trials shown through a {context}. Here is the context that you can use to make it personalizable: {content}. End it with redirecting them to a google form: {link}. In the response you generate, Just generate the final message without any additional information before or after the message. Just the message without here it is or anything else, just the message"

    else:
        prompt = f"Write a personalized message of maximum 100 words to the Reddit user named {author_name} who has shown concern in clinical trials shown through a {context}. Here is the context that you can use to make it personalizable: {content}. End it with redirecting them to a google form: {link}. In the response you generate, Just generate the final message without any additional information before or after the message. Just the message without here it is or anything else, just the message"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
    )

    message = response['choices'][0]['message']['content'].strip()
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
    post_id = row['post_id']  
    post_content = posts_df.loc[posts_df['id'] == post_id, 'body'].values[0]  
    combined_content = f"Post: {post_content}\nComment: {comment_content}"  
    sentiment = row['sentiment_category'] 
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