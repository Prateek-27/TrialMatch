import os

# Run the scrape reddit script
print("scraping reddit....")
os.system("python scripts/scrape_reddit.py")

# Run the sentiment analysis script
print('sentiment analysis....')
os.system("python scripts/sentiment_analysis.py")

# Run the generate messages script
print('personalizing messages....')
os.system("python scripts/generate_messages.py")

