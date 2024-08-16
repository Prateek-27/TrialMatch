import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


sia = SentimentIntensityAnalyzer()

posts_df = pd.read_csv('data/reddit_posts.csv')
comments_df = pd.read_csv('data/reddit_comments.csv')

# Function to get compound sentiment score
def analyze_sentiment_vader(text):
    if isinstance(text, str):  
        sentiment = sia.polarity_scores(text)
        return sentiment['compound']  
    else:
        return 0  

posts_df['sentiment'] = posts_df['body'].apply(analyze_sentiment_vader)

comments_df['sentiment'] = comments_df['body'].apply(analyze_sentiment_vader)

# Function to lable the sentiment scores
def classify_sentiment_vader(compound_score):
    if compound_score >= 0.05:
        return "positive"
    elif compound_score <= -0.05:
        return "negative"
    else:
        return "neutral"

posts_df['sentiment_category'] = posts_df['sentiment'].apply(classify_sentiment_vader)

comments_df['sentiment_category'] = comments_df['sentiment'].apply(classify_sentiment_vader)

# Save the data frame to a csv file
posts_df.to_csv('data/reddit_posts_with_sentiment.csv', index=False)
comments_df.to_csv('data/reddit_comments_with_sentiment.csv', index=False)

print("Sentiment analysis completed and results saved.")
