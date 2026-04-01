import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load clean data
CLEAN_FILE = "clean_bib_comments.csv"

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        label = 'positive'
    elif compound <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'
    
    return compound, label

def analyze_comments(comments_df):
    print("🔍 Analyzing sentiment...")

    comments_df[['compound', 'sentiment']] = comments_df['comment_text'].apply(
        lambda text: pd.Series(get_sentiment(text))
    )

    print(f"✅ Sentiment analyzed for {len(comments_df)} comments")
    print(f"\n--- Sentiment Breakdown ---")
    print(comments_df['sentiment'].value_counts())

    return comments_df

if __name__ == "__main__":
    comments_df = pd.read_csv(CLEAN_FILE)
    comments_df = analyze_comments(comments_df)
    
    print("\n--- Sample with Sentiment ---")
    print(comments_df[['comment_text', 'sentiment', 'compound']].head())
    comments_df.to_csv("clean_bib_sentiment.csv", index=False)
    print("\n✅ Saved to clean_bib_sentiment.csv")