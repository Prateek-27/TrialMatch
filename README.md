# TrialMatch: AI Powered Clinical Trial Recruitment

### Objective
The objective of TrialMatch is to ethically scrape and analyze web data, utilize sentiment analysis, and leverage AI to personalize communication. The focus is on identifying potential participants for clinical trials by analyzing sentiments expressed on Reddit.

---

## Environment Setup

1. **GitHub Repository Setup**
   - A GitHub repository named **TrialMatch** was created to manage version control and collaboration.
   - The repository was cloned locally using:
     ```bash
     git clone https://github.com/Prateek-27/TrialMatch.git
     ```

2. **Project Setup in VS Code**
   - The project was opened in Visual Studio Code (VS Code) to manage and edit files efficiently.

3. **Virtual Environment Setup**
   - A virtual environment was created to isolate project dependencies:
     ```bash
     python -m venv trial_match
     ```
   - The virtual environment was activated using:
     ```bash
     .\trial_match\Scripts\activate
     ```

4. **Installing Required Packages**
   - Essential Python packages were installed, including:
     - **PRAW**: For interacting with the Reddit API.
     - **NLTK**: For natural language processing, particularly sentiment analysis.
     - **Pandas**: For data manipulation and analysis.
     - **Dotenv**: For managing environment variables securely.
     - **VADER Lexicon**: A sentiment analysis tool from NLTK.
     - **Groq**: Used as an alternative to OpenAI for generating personalized messages due to the availability of free API access.

5. **Environment Variables Management**
   - Sensitive information, such as API keys, was managed using a `.env` file to ensure security and ease of configuration.

6. **Project Structure**
   - The project was organized into the following structure:
     - `data/`: For storing scraped data and generated messages.
     - `scripts/`: For storing the various Python scripts used throughout the project.

---

## Scrape Reddit

1. **Reddit API Setup**
   - Reddit API credentials were configured following [PRAW's official documentation](https://praw.readthedocs.io/en/stable/).
   - A `praw.Reddit` object was created to interact with Reddit, allowing for the retrieval of posts and comments from specified subreddits.

2. **Scraping Script (`scrape_reddit.py`)**
   - A dedicated script was developed to scrape data from Reddit. The script reads subreddits and keywords from `subreddits.txt` and `keywords.txt` respectively, making the scraping process flexible and customizable.
   - The script is designed to:
     - Scrape posts from specified subreddits that match the given keywords.
     - Capture relevant data fields such as the post title, body, author, etc.
     - Handle potential issues like inaccessible subreddits or API rate limits.

3. **Dynamic Input Files**
   - The use of `subreddits.txt` and `keywords.txt` allows for easy modification of the scraping parameters, enabling the focus to shift quickly between different clinical trial topics.

4. **Comment Scraping**
   - The script was enhanced to scrape comments associated with the retrieved posts, providing richer data for subsequent sentiment analysis.

5. **Data Storage**
   - The scraped data was saved in CSV format (`reddit_posts.csv` and `reddit_comments.csv`) for ease of analysis and integration with other scripts.

---

## Sentiment Analysis

1. **Sentiment Analysis Script (`sentiment_analysis.py`)**
   - The sentiment analysis was conducted using VADER, a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media.
   - The script processes the text content of both posts and comments, analyzing and categorizing them as positive, neutral, or negative based on their compound sentiment score.

2. **Classification**
   - Sentiments were classified into three categories:
     - **Positive**: Indicating a strong interest in clinical trials.
     - **Neutral**: Indicating some interest but with reservations or lack of enthusiasm.
     - **Negative**: Indicating concerns or opposition to clinical trials.
   - This classification was crucial in tailoring the personalized messages to each user's sentiment.

3. **Saving Results**
   - The results of the sentiment analysis were saved in CSV files (`reddit_posts_with_sentiment.csv` and `reddit_comments_with_sentiment.csv`). These files were then used to generate personalized messages.

---

## Personalized Messaging

1. **Message Generation Script (`generate_messages.py` and `generate_messages_openai.py`)**
   - **Primary Approach with Groq**:
     - Due to the availability of free access, Groq was used to generate personalized messages based on the sentiment analysis results.
     - The script tailors messages to the user's sentiment, with different tones and calls to action depending on whether the sentiment is positive, neutral, or negative.
     - The request utilizes smart prompt engineering to personalize the message such as addressing the user directly using their username, adding context, etc.
   - **Alternative with OpenAI**:
     - Although Groq was the primary tool used, a script (`generate_messages_openai.py`) was also provided for generating messages using the OpenAI API. This script allows for seamless integration with OpenAI's GPT models if API tokens become available.

2. **Combining Post and Comment Content**
   - For users who had commented on posts, the script combined the original post content with the comment content to provide richer context for the personalized messages.

3. **Google Form** 
   - A Google Form link was included at the end of each personalized message, directing users to a form where they could express their interest in or concerns about participating in clinical trials.
     
4. **Output**
   - The generated messages were saved into a CSV file (`personalized_messages.csv`), ready for review or potential use in outreach.

---

## Sending Messages (Optional)

1. **Message Sending Script (`send_messages.py`)**
   - The script reads the personalized messages from the CSV file and sends them to the respective Reddit users using PRAW.
   - It includes logic to handle different scenarios:
     - **Direct Messages**: Attempted first, subject to the recipient's settings.
     - **Chat Requests**: Used as a fallback if direct messages are restricted.
   - **Error Handling**: The script gracefully handles errors such as restricted messaging and API rate limits, logging any issues for review.

2. **Ethical Note**
   - While the script demonstrates the ability to send messages, this feature should be used with caution and only after careful consideration of ethical implications and user consent. Hence, in my application, I have not executed this script in the main.py so that the messages are not sent. 

---

## Ethical Considerations

1. **Public Data Usage**
   - Data was sourced from Reddit, a public platform where users voluntarily share information. However, the project adhered to strict ethical standards, avoiding the collection of personally identifiable information (PII).

2. **Privacy**
   - The project focused on analyzing publicly available data without intruding on users' privacy. No PII, such as names or email addresses, was collected or used.

3. **Demonstration and Consent**
   - The project emphasized the generation of personalized messages as a demonstration of capability. The actual sending of messages was conducted in a controlled manner, and the approach respects the need for user consent before any real-world application.

---

## Final Notes

   - The scripts effectively perform the tasks of scraping Reddit data, analyzing sentiment, and generating personalized messages. Each component of the project is designed to work together seamlessly, from data collection to message generation and potential outreach.

   - The codebase is well-organized and modular, with clear separation of concerns across different scripts. Each script is documented, making the code easy to understand and maintain. The use of environment variables and error handling ensures the code is robust and secure.

   - **Adaptation of Groq**: The decision to use Groq instead of OpenAI for generating personalized messages due to the lack of available API keys was a practical and innovative solution. Despite this, a script for OpenAI was also provided, showcasing flexibility and forward-thinking.
     
   - **Dynamic Input Handling**: The use of `subreddits.txt` and `keywords.txt` for flexible data scraping is another innovative aspect, allowing the project to adapt quickly to different clinical trial focuses.
     
   - **Advanced Prompt Engineering**: The project employed sophisticated prompt engineering techniques to craft highly personalized messages. By dynamically incorporating user-specific details such as their Reddit username and contextual information (e.g., the content of their post or the combination of their comment and post), the messages were made more relevant and engaging. This approach ensured that each message resonated with the recipient's unique experience and interaction on the platform, thereby enhancing the overall effectiveness of the communication.

   - **Google Form Integration**: A Google Form link was included at the end of each personalized message, directing users to a form where they could express their interest in or concerns about participating in clinical trials. This facilitated an additional layer of interaction, enabling users to provide feedback or show interest conveniently.

   - The project is a model of how to responsibly conduct data scraping and user engagement. By prioritizing privacy and user consent, the project aligns with best practices in ethical AI and data science.

---

### Conclusion

TrialMatch exemplifies how AI and sentiment analysis can be harnessed to improve clinical trial recruitment while maintaining high ethical standards. The project combines various technologies to create a robust, adaptable, and ethical solution for identifying and engaging potential clinical trial participants. The careful consideration of privacy, ethical messaging, and innovative use of available tools makes TrialMatch a standout project in AI-driven recruitment efforts.
